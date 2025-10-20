# Usage: python 580vnx/decomp_.py "./hex_ropchain/<input_hex.txt>" "./asm_ropchain/<output.asm>"
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from modules.libdecompiler import get_disas, get_commands, decompile

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python 580vnx/decomp_.py "./hex_ropchain/<input_hex.txt>" "./asm_ropchain/<output.asm>"')
        sys.exit()

    inp, outp = sys.argv[1:3]

    if not os.path.exists(inp):
        print(f"Input not found: {inp}")
        sys.exit()

    start_ram = 0xD000
    end_ram = 0xF000

    base_dir = os.path.dirname(__file__)
    model_dir = os.path.join(base_dir)

    disas_path = os.path.join(model_dir, "disas.txt")
    gadgets_path = os.path.join(model_dir, "gadgets.txt")
    labels_path = os.path.join(model_dir, "labels.txt")

    for path in [disas_path, gadgets_path, labels_path]:
        if not os.path.exists(path):
            print(f"[!] Missing required model file: {path}")
            sys.exit()

    disas = get_disas(disas_path)
    gadgets = get_commands(gadgets_path)
    labels = get_commands(labels_path)

    output = decompile(inp, outp, disas, gadgets, labels, start_ram, end_ram)

    os.makedirs(os.path.dirname(outp) or '.', exist_ok=True)
    with open(outp, 'w', encoding='utf-8') as w:
        w.write(''.join(output))

    print(f"[+] Decompiled successfully -> {outp}")