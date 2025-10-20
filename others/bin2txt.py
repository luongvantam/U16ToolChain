#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: python bin2txt.py bin2txt input.bin
#       python bin2txt.py txt2bin-hex input.txt
#       python bin2txt.py txt2bin-ascii input.txt
import sys

def bin2txt(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    with open(output_file, 'w') as f:
        for i in range(0, len(data), 16):
            line = ' '.join(f"{b:02X}" for b in data[i:i+16])
            f.write(line + '\n')

def txt2bin_hex(input_file, output_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            for p in parts:
                try:
                    data.append(int(p, 16))
                except ValueError:
                    continue
    with open(output_file, 'wb') as f:
        f.write(bytes(data))

def txt2bin_ascii(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(output_file, 'wb') as f:
        f.write(content.encode('utf-8'))

if __name__ == "__main__":
    try:
        cmd = sys.argv[1].lower()
        inp = sys.argv[2]
        
        if cmd == 'bin2txt':
            outp = '../output.txt'
            bin2txt(inp, outp)
        elif cmd == 'txt2bin-hex':
            outp = '../output.bin'
            txt2bin_hex(inp, outp)
        elif cmd == 'txt2bin-ascii':
            outp = '../output.bin'
            txt2bin_ascii(inp, outp)
    except:
        pass