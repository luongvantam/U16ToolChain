#!/usr/bin/env python3
import sys
import re
import argparse

MAX_TOKENS = 21
HEX_RE = re.compile(r'^[0-9A-Fa-f]{1,2}$')

byte_table = [
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1,
    2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]

def normalize(raw_tokens):
    toks = [t.strip().upper() for t in raw_tokens if t.strip()]
    for t in toks:
        if not HEX_RE.match(t):
            print(f"[ERROR] Invalid hex byte: {t}")
    return [t.zfill(2).upper() for t in toks]

def split_hex_bytes(hex_string):
    hex_string = hex_string.strip().replace(' ', '')
    if len(hex_string) % 2 != 0:
        print("[ERROR] Hex string must have an even number of characters.")
    return [hex_string[i:i+2].upper() for i in range(0, len(hex_string), 2)]

def contains_letter(tok):
    return any(ch in 'ABCDEF' for ch in tok)

def parse_and_transform(hex_string):
    global byte_table
    raw = split_hex_bytes(hex_string)
    normalized_toks = normalize(raw)

    byte_1 = []
    checked_toks = []
    i = 0
    while i < len(normalized_toks):
        t = normalized_toks[i]
        val = int(t, 16)

        if t.upper().startswith("F"):
            if i + 1 >= len(normalized_toks):
                i += 1
                continue
            pair_next = normalized_toks[i + 1]
            checked_toks.append(t)
            checked_toks.append(pair_next)
            byte_1.append(t + pair_next)
            i += 2
            continue

        if byte_table[val] == 0:
            return "[ERROR] Contains invalid byte 00", byte_1
        elif byte_table[val] == 1:
            checked_toks.append(t)
            byte_1.append(t)
        i += 1

    all_toks = ['00', '00'] + checked_toks

    i = 0
    while i < len(all_toks):
        pos_in_block = i % 8
        if pos_in_block in (5, 7) and contains_letter(all_toks[i]):
            insert_pos = i
            if i > 0 and all_toks[i-1].startswith('F'):
                insert_pos = i - 1
            all_toks.insert(insert_pos, '30')
            i += 1
        i += 1

    blocks = []
    current_block = []
    for b in all_toks:
        if len(current_block) == 8:
            blocks.append(current_block)
            current_block = []
        current_block.append(b)
    if current_block:
        blocks.append(current_block)

    if blocks:
        if '23' not in blocks[-1]:
            blocks[-1].append('23')
    else:
        blocks.append(['23'])

    output_parts = []
    names = ['A', 'B', 'C']
    for idx, block in enumerate(blocks):
        if not block:
            continue
        if (len(block) == 8 and idx < len(blocks)-1) or (block[-1] == '23'):
            block = block[:-1] + ['x10^', block[-1]]
        if idx < 3:
            output_parts.append(f"{names[idx]} = 1. {' '.join(block)}")
    
    output = "\n".join(output_parts)
    return output, byte_1

def main():
    parser = argparse.ArgumentParser(description="Hex Splitter for fx580vnx")
    parser.add_argument("hex_input", nargs="+", help="Hex string to transform (e.g., 'A1 B2 C3' or 'A1B2C3')")
    
    args = parser.parse_args()
    input_str = "".join(args.hex_input)

    try:
        out, byte1 = parse_and_transform(input_str)
        print(out)
        
        if "[ERROR]" not in out:
            if byte1:
                print(f"\nNumber of bytes to assign: {' '.join(byte1)}")
            else:
                print("\nNo bytes to assign.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()