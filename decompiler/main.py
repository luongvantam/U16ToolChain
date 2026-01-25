#!/usr/bin/env python3
import os
import sys
import importlib.util
from libdecompiler import get_disas, get_commands, decompile

def load_model_config(model_name):
    """Dynamically imports config.py from the specified model folder."""
    config_path = os.path.join(model_name, "config.py")
    
    if not os.path.exists(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    # Magic to import a file by path
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

def main():
    if len(sys.argv) < 4:
        print('Usage: python main.py <model_name> <input_hex.txt> <output.asm>')
        sys.exit(1)

    model_name, inp, outp = sys.argv[1:4]

    if not os.path.exists(inp):
        print(f"[ERROR] Input file not found: {inp}")
        sys.exit(1)

    cfg = load_model_config(model_name)
    disas = get_disas(os.path.join(model_name, 'disas.txt'))
    gadgets = get_commands(os.path.join(model_name, 'gadgets.txt'))
    labels = get_commands(os.path.join(model_name, 'labels.txt'))

    output = decompile(inp, outp, disas, gadgets, labels, cfg.start_ram, cfg.end_ram)
    os.makedirs(os.path.dirname(outp) or '.', exist_ok=True)
    with open(outp, 'w', encoding='utf-8') as w:
        w.write(''.join(output))
    
    print(f"[SUCCESS] Decompilation finished. Saved to: {outp}")

if __name__ == '__main__':
    main()