#!/bin/bash

mkdir -p hex_ropchain
mkdir -p asm_ropchain

while true; do
    clear
    echo "╔════════════════════════════════════════╗" 
    echo "║             U16ToolChain               ║"
    echo "╚════════════════════════════════════════╝"

    read -p "Enter your filename to decompile (only fx580vnx): " filename
    hex_file_path="hex_ropchain/${filename}.txt"
    asm_file_path="asm_ropchain/${filename}.asm"
    decomp_script="580vnx/decomp_.py"

    if [ ! -f "$hex_file_path" ]; then
        echo "Error: File '$hex_file_path' not found!"
        echo "Press any key to try again..."
        read -n 1 -s
        continue
    fi

    echo "Decompiling '${filename}.txt'..."
    python "$decomp_script" "$hex_file_path" "$asm_file_path"

    if [ $? -eq 0 ]; then
        echo -e "\nDecompilation complete. Output saved to '$asm_file_path'"
    else
        echo "An error occurred while running the decompiler script."
    fi

    echo "Press to continue..."
    read -n 1 -s
done