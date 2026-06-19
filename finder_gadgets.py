#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: python finder_gadgets.py [disas_file] [-p pattern_file | -s "pattern string" | --stdin] [-c context_lines]
# Usage basic: python finder_gadgets.py [disas_file]
import argparse
import sys

def normalize_line(line: str) -> str:
    return line.rstrip('\n')

def split_and_normalize_patterns(s: str) -> list:
    if not s:
        return []
    s = s.strip()
    if "\\n" in s and "\n" not in s:
        parts = s.split("\\n")
        return [p.strip().lower() for p in parts if p.strip()]
    lines = s.splitlines()
    return [ln.strip().lower() for ln in lines if ln.strip()]

def read_disas_file(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.readlines()
    except FileNotFoundError:
        print(f"[!] File does not exist: {path}", file=sys.stderr)
        sys.exit(2)

def find_matches(content_lines: list, patterns: list) -> list:
    matches = []
    n = len(content_lines)
    if not patterns:
        return matches

    low_lines = [ln.lower() for ln in content_lines]

    for i in range(n):
        found_idx = 0
        collected = []
        for j in range(i, n):
            low = low_lines[j]
            if patterns[found_idx] in low:
                collected.append(content_lines[j].rstrip("\n"))
                found_idx += 1
                if found_idx >= len(patterns):
                    matches.append((i, collected.copy()))
                    break
            else:
                break
    return matches

def group_by_function(content_lines: list, matches: list) -> list:
    start_map = {}
    for start_idx, block in matches:
        start_map.setdefault(start_idx, []).append(block)

    out_lines = []
    current_func = None
    n = len(content_lines)
    for idx in range(n):
        stripped = content_lines[idx].strip()
        if stripped.endswith(':') and '.' not in stripped:
            current_func = stripped
        if idx in start_map:
            for block in start_map[idx]:
                if current_func:
                    out_lines.append(f"In function {current_func}")
                else:
                    out_lines.append("In function <unknown>")
                out_lines.extend(block)
                out_lines.append("")
    return out_lines

def interactive_read_patterns() -> list:
    print("Enter the gadget pattern line by line (type 'end' to finish):")
    lines = []
    try:
        while True:
            ln = input().rstrip("\n")
            if ln.strip().lower() == "end":
                break
            if ln.strip():
                lines.append(ln)
    except EOFError:
        pass
    return [l.strip().lower() for l in lines if l.strip()]

def main():
    parser = argparse.ArgumentParser(description="find_gadget - find gadget in disassembly file")
    parser.add_argument("disas", nargs="?", default="../assets/data/fx580vnx.txt",
        help="path to disassembly file (default: ../assets/data/fx580vnx.txt)")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", "--pattern-file", help="read pattern from file (one pattern per line)")
    group.add_argument("-s", "--string", help="pattern string (use \\n to separate lines)")
    parser.add_argument("--stdin", action="store_true", help="read pattern from stdin (pipe)")
    parser.add_argument("-c", "--context", type=int, default=0,
        help="number of context lines after match (default 0)")
    args = parser.parse_args()

    patterns = []
    if args.stdin:
        data = sys.stdin.read()
        patterns = split_and_normalize_patterns(data)
    elif args.pattern_file:
        try:
            with open(args.pattern_file, "r", encoding="utf-8", errors="ignore") as pf:
                data = pf.read()
            patterns = split_and_normalize_patterns(data)
        except Exception as e:
            print(f"[!] Cannot read pattern file: {e}", file=sys.stderr)
            sys.exit(3)
    elif args.string:
        patterns = split_and_normalize_patterns(args.string)
    else:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            patterns = split_and_normalize_patterns(data)
        else:
            patterns = interactive_read_patterns()

    if not patterns:
        print("[!] No pattern has been imported yet.", file=sys.stderr)
        sys.exit(4)

    disas_lines = read_disas_file(args.disas)
    matches = find_matches(disas_lines, patterns)

    if not matches:
        print("No matching gadgets found.")
        sys.exit(0)

    grouped = group_by_function(disas_lines, matches)

    if args.context > 0 and grouped:
        enriched = []
        for start_idx, block in matches:
            func_name = "<unknown>"
            for k in range(start_idx, -1, -1):
                s = disas_lines[k].strip()
                if s.endswith(':') and '.' not in s:
                    func_name = s
                    break
            enriched.append(f"In function {func_name}")
            for line in block:
                enriched.append(line)
            j = start_idx + len(block)
            for c in range(args.context):
                if j + c < len(disas_lines):
                    enriched.append(disas_lines[j + c].rstrip("\n"))
            enriched.append("")
        out = "\n".join(enriched).strip()
    else:
        out = "\n".join(grouped).strip()

    print(out)

if __name__ == "__main__":
    main()
