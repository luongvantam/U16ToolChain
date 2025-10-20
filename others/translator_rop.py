# Usage: python translator_rop.py <source_model> <target_model> <address>
import sys
import os
import re

DATA_DIR = "../assets/data"

def load_file(model):
    path = os.path.join(DATA_DIR, f"{model}.txt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def token_key(line):
    parts = re.split(r"\s+", line.strip())
    if len(parts) > 1:
        return parts[1][:4].lower()
    return ""

def compare_context(src, dst, si, ti, offsets):
    for off in offsets:
        if not (0 <= si+off < len(src) and 0 <= ti+off < len(dst)):
            return False
        if token_key(src[si+off]) != token_key(dst[ti+off]):
            return False
    return True

def translate_levels(src_lines, dst_lines, search):
    search_low = search.lower()
    for si, line in enumerate(src_lines):
        if search_low in line.lower():
            for ti in range(len(dst_lines)):
                if compare_context(src_lines, dst_lines, si, ti, [-2,-1,0,1,2]):
                    return dst_lines[ti]
            for ti in range(len(dst_lines)):
                if compare_context(src_lines, dst_lines, si, ti, [-1,0,1]):
                    return dst_lines[ti]
            for ti in range(len(dst_lines)):
                if compare_context(src_lines, dst_lines, si, ti, [0,1,2]):
                    return dst_lines[ti]
            for ti in range(len(dst_lines)):
                if compare_context(src_lines, dst_lines, si, ti, [0,1]):
                    return dst_lines[ti]
    return None

def normalize_address(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("0x", "").replace("h", "")
    if ":" in s:
        bank, addr = s.split(":", 1)
    else:
        bank, addr = s[0], s[1:]
    addr = addr.zfill(4).upper()
    return f"{bank.upper()}:{addr}H"

def decrement_address(addr: str) -> str:
    match = re.match(r"([0-9A-F]+):([0-9A-F]{4})H", addr, re.IGNORECASE)
    if not match:
        return addr
    bank, offset = match.groups()
    value = int(offset, 16)
    if value == 0:
        return addr
    new_value = value - 1
    return f"{bank.upper()}:{new_value:04X}H"

def main():
    if len(sys.argv) < 4:
        print("Usage: python translator_rop.py <source_model> <target_model> <address>")
        sys.exit()

    src_model = sys.argv[1]
    dst_model = sys.argv[2]
    raw_input = sys.argv[3]

    src_lines = load_file(src_model)
    dst_lines = load_file(dst_model)

    formatted = normalize_address(raw_input)

    attempts = 0
    result = None
    current_addr = formatted
    while attempts < 4:
        result = translate_levels(src_lines, dst_lines, current_addr)
        if result:
            break
        current_addr = decrement_address(current_addr)
        attempts += 1

    if result:
        print(result)
    else:
        print(f"No translations found for: {raw_input} (normalized {formatted}) after {attempts} attempts")

if __name__ == "__main__":
    main()