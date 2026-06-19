#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os

def bin_to_txt(input_file, output_file):
    """Converts binary file to a space-separated Hex text file."""
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        with open(output_file, 'w', encoding='utf-8') as f:
            for i in range(0, len(data), 16):
                # Formats 16 bytes per line as XX XX XX...
                line = ' '.join(f"{b:02X}" for b in data[i:i+16])
                f.write(line + '\n')
        print(f"[SUCCESS] Converted binary to text: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to convert: {e}")

def txt_to_bin_hex(input_file, output_file):
    """Converts a Hex text file back into a binary file."""
    data = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                for p in parts:
                    try:
                        data.append(int(p, 16))
                    except ValueError:
                        continue
        with open(output_file, 'wb') as f:
            f.write(bytes(data))
        print(f"[SUCCESS] Converted hex text to binary: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to convert: {e}")

def txt_to_bin_ascii(input_file, output_file):
    """Encodes a standard text file into binary using UTF-8."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(output_file, 'wb') as f:
            f.write(content.encode('utf-8'))
        print(f"[SUCCESS] Converted ASCII text to binary: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to convert: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Binary/Text Conversion Utility CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bin_tool.py bin2txt input.bin -o result.txt
  python bin_tool.py hex2bin input.txt
  python bin_tool.py ascii2bin notes.txt -o data.bin
        """
    )

    # Positional arguments
    parser.add_argument(
        "mode", 
        choices=["bin2txt", "hex2bin", "ascii2bin"], 
        help="Conversion mode"
    )
    parser.add_argument("input", help="Path to the source file")
    
    # Optional argument for output path
    parser.add_argument("-o", "--output", help="Path to the output file (optional)")

    args = parser.parse_args()

    # Determine default output filename if not provided
    if not args.output:
        if args.mode == "bin2txt":
            output_path = "output.txt"
        else:
            output_path = "output.bin"
    else:
        output_path = args.output

    # Execute based on mode
    if args.mode == "bin2txt":
        bin_to_txt(args.input, output_path)
    elif args.mode == "hex2bin":
        txt_to_bin_hex(args.input, output_path)
    elif args.mode == "ascii2bin":
        txt_to_bin_ascii(args.input, output_path)

if __name__ == "__main__":
    main()