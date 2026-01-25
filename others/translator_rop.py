import sys
import os
import re
import argparse
from typing import List, Optional, Set

# --- CONFIGURATION ---
# Default directory containing the model text files
DATA_DIR = "../assets/data"

def load_file(model: str) -> List[str]:
    """Loads content from the model file within the data directory."""
    path = os.path.join(DATA_DIR, f"{model}.txt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip() for line in f if line.strip()]

def extract_address_from_line(line: str) -> str:
    """Extracts a memory address (e.g., 1:7B34H) from a given line."""
    match = re.search(r"([0-9A-F]+:[0-9A-F]{4}H)", line.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return ""

def extract_instruction_payload(line: str) -> str:
    """Extracts the Opcode and Operand following the address."""
    addr_match = re.search(r"([0-9A-F]+:[0-9A-F]{4}H)", line.strip(), re.IGNORECASE)
    if not addr_match:
        return ""
    
    # Get the part of the string after the address
    payload_part = line[addr_match.end():].strip()
    # Normalize whitespaces and take the first two components (e.g., MOV R1)
    parts = re.sub(r'\s+', ' ', payload_part).strip().split(maxsplit=2)
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}".upper()
    return ""

def get_source_chain(src_lines: List[str], search_addr: str) -> List[str]:
    """Finds an instruction chain starting from a specific address."""
    search_low = search_addr.lower()
    start_index = -1
    for i, line in enumerate(src_lines):
        if search_low in line.lower():
            start_index = i
            break
    
    if start_index == -1:
        return []

    target_payload = extract_instruction_payload(src_lines[start_index])
    if not target_payload:
        return []

    # Look for the next valid instruction (skipping junk/empty lines)
    next_payload = ""
    for i in range(start_index + 1, len(src_lines)):
        next_payload = extract_instruction_payload(src_lines[i])
        if next_payload:
            break
            
    chain = [target_payload.upper()]
    if next_payload:
        chain.append(next_payload.upper())
    return chain

def translate_by_chain_match(src_chain: List[str], dst_lines: List[str]) -> List[str]:
    """Finds lines in the destination model that match the source instruction chain."""
    if not src_chain:
        return []
    results: Set[str] = set()
    n_chain = len(src_chain)

    for i in range(len(dst_lines)):
        dst_payload_start = extract_instruction_payload(dst_lines[i])
        if dst_payload_start.upper() != src_chain[0]:
            continue
        
        if n_chain == 1:
            results.add(dst_lines[i])
            continue
        
        # If the chain has 2 instructions, verify the sequence
        if n_chain == 2:
            next_payload = ""
            for j in range(i + 1, len(dst_lines)):
                next_payload = extract_instruction_payload(dst_lines[j])
                if next_payload:
                    break
            if next_payload.upper() == src_chain[1]:
                results.add(dst_lines[i])
                
    return sorted(list(results), key=extract_address_from_line)

def normalize_address(s: str) -> str:
    """Normalizes various address formats to X:YYYYH."""
    s = s.strip().lower().replace("0x", "").replace("h", "")
    if ":" in s:
        bank, addr = s.split(":", 1)
    else:
        # Fallback for raw strings where the first char is the bank
        if len(s) >= 5:
            bank, addr = s[0], s[1:]
        else:
            raise ValueError(f"Invalid address format: {s}")
    
    return f"{bank.upper()}:{addr.zfill(4).upper()}H"

def hex_to_address(hex_str: str) -> str:
    """Converts 4-byte raw hex (Little Endian) to a formatted address."""
    clean = ''.join(re.findall(r'[0-9A-Fa-f]{2}', hex_str))
    if len(clean) != 8:
        raise ValueError("Hex input must be 4 bytes (8 characters)")
    
    # Logic based on your specific hex-to-address mapping
    b1, b2, b3, b4 = clean[0:2], clean[2:4], clean[4:6], clean[6:8]
    offset = f"{b2}{b1}".upper().zfill(4)
    bank = int(b3[1], 16)
    return f"{bank:X}:{offset}H"

def decrement_address(addr: str) -> str:
    """Decrements the offset by 1 (used for scanning backwards for gadgets)."""
    match = re.match(r"([0-9A-F]+):([0-9A-F]{4})H", addr, re.IGNORECASE)
    if not match: return addr
    bank, offset = match.groups()
    val = int(offset, 16)
    return f"{bank.upper()}:{(val - 1 if val > 0 else 0):04X}H"

def extract_offset_int(addr: str) -> int:
    match = re.search(r":([0-9A-F]{4})H", addr, re.IGNORECASE)
    return int(match.group(1), 16) if match else -1

def find_closest_line(results: List[str], target_addr: str) -> str:
    """Identifies the result line with the closest offset to the original address."""
    if not results: return ""
    target_offset = extract_offset_int(target_addr)
    if target_offset == -1: return results[0]
    
    best_line = results[0]
    min_diff = float('inf')
    
    for line in results:
        curr_addr = extract_address_from_line(line)
        curr_offset = extract_offset_int(curr_addr)
        if curr_offset != -1:
            diff = abs(curr_offset - target_offset)
            if diff < min_diff:
                min_diff = diff
                best_line = line
    return best_line

def process_translation(src_model: str, dst_model: str, addresses: List[str]):
    """Main logic to process and print translation results to console."""
    try:
        src_lines = load_file(src_model)
        dst_lines = load_file(dst_model)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    print("=" * 60)
    print(f"ROP TRANSLATOR: {src_model} -> {dst_model}")
    print("=" * 60)

    for raw_addr in addresses:
        try:
            # Check if input is raw hex (8 chars) or a standard address
            if re.fullmatch(r'([0-9A-Fa-f]{2}\s*){4}', raw_addr.strip()) or len(raw_addr.strip()) == 8:
                formatted_addr = hex_to_address(raw_addr)
            else:
                formatted_addr = normalize_address(raw_addr)
        except Exception:
            print(f"\n[!] Gadget {raw_addr}: Invalid address format. Skipping...")
            continue

        print(f"\n{"-" * 22} Gadget {formatted_addr} {"-" * 22}")
        
        # Search for source chain (attempt 4-byte backscan)
        source_chain = []
        current_search = formatted_addr
        for _ in range(4):
            source_chain = get_source_chain(src_lines, current_search)
            if source_chain: break
            current_search = decrement_address(current_search)

        if not source_chain:
            print(f"  [-] No matching ROP instructions found in source file.")
            continue

        # Find matches in destination
        results = translate_by_chain_match(source_chain, dst_lines)
        
        if results:
            closest_line = find_closest_line(results, formatted_addr)
            for res in results:
                marker = "      [closest option]" if res == closest_line else ""
                print(f"  [+] {res}{marker}")
        else:
            print(f"  [-] No translations found in {dst_model} for this chain.")

def main():
    parser = argparse.ArgumentParser(
        description="ROP Gadget Translator"
    )
    parser.add_argument("src", help="Source model name (e.g., firmware_v1)")
    parser.add_argument("dst", help="Target model name (e.g., firmware_v2)")
    parser.add_argument("addrs", nargs="+", help="List of addresses to translate (space separated)")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Flatten inputs in case user uses comma/semicolon separation
    input_addresses = []
    for a in args.addrs:
        input_addresses.extend(re.split(r'[;,]+', a))
    
    input_addresses = [a.strip() for a in input_addresses if a.strip()]

    process_translation(args.src, args.dst, input_addresses)

if __name__ == "__main__":
    main()