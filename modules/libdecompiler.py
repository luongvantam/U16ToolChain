# pyu16decomp v2.1
# Created by luongvantam last created: 11:46 AM 08-23-2025(GMT+7)
# Last modified: 3:05 PM 10-14-2025(GMT+7)
import os
import sys
import re

def get_disas(file_path: str) -> dict:
    """
    Đọc file disas.txt, trả về dict {addr: instruction}
    Hỗ trợ định dạng kiểu:
    1:7B34H	F02E			POP XR0
    """
    data = {}

    if not os.path.exists(file_path):
        return data
    
    def parse_addr(tok: str):
        tok = tok.strip()
        if not tok:
            return None
        if ':' in tok:
            seg, off = tok.split(':', 1)
            off = off.rstrip('Hh').strip()
            seg = seg.strip()
            try:
                seg_v = int(seg, 16) if seg else 0
                off_v = int(off, 16)
                return (seg_v << 16) | off_v
            except Exception:
                return None
        t = tok.rstrip('Hh').rstrip(':')
        if re.fullmatch(r'[0-9A-Fa-f]+', t):
            try:
                return int(t, 16)
            except Exception:
                return None
        return None
    with open(file_path, 'r', encoding='utf-8') as fh:
        for ln in fh:
            line = ln.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            addr_tok = parts[0]
            addr = parse_addr(addr_tok)
            if addr is None:
                continue
            instr = ' '.join(parts[2:]) if len(parts) >= 3 else ' '.join(parts[1:])
            instr = instr.strip()
            data[addr] = instr
    return data


def get_commands(file_path: str) -> dict:
    """
    Đọc file gadget.txt hoặc labels.txt, trả về dict {addr: line}
    Hỗ trợ định dạng kiểu:
    17bda       pop qr0
    """
    data = {}
    if not os.path.exists(file_path):
        return data
    with open(file_path, 'r', encoding='utf-8') as fh:
        for ln in fh:
            line = ln.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            key = parts[0].lower().removeprefix('@')
            try:
                addr = int(key, 16)
            except Exception:
                continue
            data[addr] = parts[1].strip()
    return data


def load_hex_buffer(lines):
    """
    Chuyển 1 chuỗi hex có xuống dòng, có dấu cách các thứ thành chuỗi liền ví dụ
    34 7B 31 30 30 30 30 30
    thành
    347B313030303030
    """
    joined = ' '.join(line.strip() for line in lines if line.strip())
    tokens = re.findall(r'[0-9A-Fa-f]{2}', joined)
    return ''.join(tokens).lower()


def swap_bytes_and_convert(outp, hex8: str) -> int:
    """
    Đổi endian 4 byte, ví dụ 34 7B 31 30 -> 347B3130 (ở load_hex_buffer()) -> 30317B34
    """
    s = hex8.strip()
    if len(s) != 8:
        with open(outp, 'w', encoding='utf-8') as err_file:
            err_file.write(f"need 8 hex chars")
        sys.exit()
    b1 = s[0:2]
    b2 = s[2:4]
    b3 = s[4:6]
    addr_hex = f"{b3[1]}{b2}{b1}"
    return int(addr_hex, 16) & 0xFFFFF


def reg_bytes(reg: str) -> int:
    """
    Trả về số byte của một thanh ghi
    Ví dụ:
    XR0 -> 4
    ER4 -> 2
    """
    r = reg.lower()
    if r.startswith('qr'): return 8
    if r.startswith('xr'): return 4
    if r.startswith('er') or r.startswith('ea'): return 2
    if r.startswith('r'): return 2
    return 0


def consume_pop_chain_from_disas(addr, disas, hex_buffer, idx, state=None, max_instr=50):
    """
    Phân tích disas để xác định các giá trị mà gadget sẽ lấy từ stack (operand chain)
    """
    out = [f"call 0x{addr:X}"]
    total_bytes_for_print = 0
    cur = addr
    push_stack = []
    count_instr = 0

    while cur in disas and count_instr < max_instr:
        inst = disas[cur].strip().lower()
        count_instr += 1

        if inst.startswith('push '):
            reg = inst.split()[1]
            push_stack.append(reg)
            cur += 2
            continue

        if inst.startswith('pop '):
            reg = inst.split()[1]
            if reg == 'pc':
                break
            if reg in push_stack:
                push_stack.remove(reg)
            else:
                total_bytes_for_print += reg_bytes(reg)
            cur += 2
            continue

        inst_lower = inst.strip()
        if inst_lower == 'b leave' or inst_lower.endswith('leave'):
            total_bytes_for_print += 12
            if state:
                state.add_to_sp(12)
            cur += 2
            continue

        if inst.startswith('rt'):
            break

        if inst.startswith('bl ') or inst.startswith('b '):
            break

        cur += 2

    if total_bytes_for_print > 0 and idx + total_bytes_for_print*2 <= len(hex_buffer):
        blob = hex_buffer[idx: idx + total_bytes_for_print*2]
        spaced = ' '.join(blob[j:j+2] for j in range(0, len(blob), 2))
        out.append(f"hex {spaced}")
        idx += total_bytes_for_print*2

    return out, idx


def resolve_address(addr, gadgets, disas, labels, max_fallback=4):
    """
    Tìm gadget trong disas nếu không thấy sẽ trừ 1 để tìm tiếp (nếu trừ quá 4 lần sẽ ngừng và ghi trực tiếp)
    """
    cur = addr
    attempts = 0
    while cur >= 0 and attempts <= max_fallback:
        if cur in gadgets or cur in disas or cur in labels:
            return cur
        cur -= 1
        attempts += 1

    return addr
            
class DecompilerState:
    def __init__(self):
        self.regs = {}
        self.sp = None
        self.org = None
    def set_reg(self, reg, value):
        self.regs[reg.lower()] = value
    def get_reg(self, reg):
        return self.regs.get(reg.lower())
    def set_sp_from_reg(self, reg):
        val = self.get_reg(reg)
        if val is not None:
            self.sp = val
        return self.sp
    def add_to_sp(self, offset):
        if self.sp is not None:
            self.sp += offset
        return self.sp
    def set_org(self, value):
        self.org = value
    def update_position(self, size):
        if self.sp is not None:
            self.sp += size
        return self.sp
state = DecompilerState()

def decompile(inp, outp, disas, gadgets, labels, start_ram, end_ram, output_lines = []):
    """
    Hàm chính để có thể decomplile
    """
    with open(inp, 'r', encoding='utf-8') as fh_in:
        raw_content = fh_in.read()

    content_to_process = raw_content
    first_line_parts = raw_content.split('\n', 1)
    if first_line_parts[0].upper().startswith('ADDR '):
        try:
            parts = first_line_parts[0].split(maxsplit=2)
            addr_str = parts[1].rstrip(':')
            addr_val = int(addr_str, 16)

            if not (start_ram <= addr_val <= end_ram):
                with open(outp, 'w', encoding='utf-8') as err_file:
                    err_file.write(f"Invalid org address 0x{addr_val:X}, must be in range 0x{start_ram:X}-0x{end_ram:X}\n")
                sys.exit()
            
            output_lines.append(f"org 0x{addr_val:X}\n\n")
            state.set_org(addr_val)

            hex_data_from_addr = parts[2].strip() if len(parts) > 2 else ''
            rest_of_file = first_line_parts[1] if len(first_line_parts) > 1 else ''
            content_to_process = hex_data_from_addr + rest_of_file
        except Exception as e:
            with open(outp, 'w', encoding='utf-8') as err_file:
                err_file.write(f"Failed to parse org address: {e}")
            sys.exit()
    else:
        output_lines.append(f"org 0xE9E0\n\n")
    
    normalized_string = re.sub(r'\s+', '', content_to_process)
    segments = re.split(r'(\[.*?\]|\(.*?\))', normalized_string)
    
    for segment in segments:
        if not segment:
            continue
        
        if segment.startswith('[') and segment.endswith(']'):
            clean_segment = segment.strip('[]')
            spaced = ' '.join(clean_segment[j:j+2] for j in range(0, len(clean_segment), 2))
            output_lines.append(f"hex {spaced}\n")
            bytes_consumed = len(clean_segment) // 2
            state.update_position(bytes_consumed)
        elif segment.startswith('(') and segment.endswith(')'):
            text_content = segment.strip('()')
            output_lines.append(f'note "{text_content}"\n')
            bytes_consumed = len(text_content)
            state.update_position(bytes_consumed)
        else:
            hex_buffer = load_hex_buffer([segment])
            i = 0
            n = len(hex_buffer)

            while i + 8 <= n:
                chunk = hex_buffer[i:i+8]
                try:
                    raw_addr = swap_bytes_and_convert(outp ,chunk)
                    addr = resolve_address(raw_addr, gadgets, disas, labels)
                except Exception as e:
                    with open(outp, 'w', encoding='utf-8') as err_file:
                        err_file.write(f"Failed to parse chunk {chunk} at index {i}: {e}")
                    sys.exit()

                i += 8
                state.update_position(4)

                if addr in labels:
                    line = labels[addr]
                    output_lines.append(f"{line}\n")
                    low = line.lower()
                    if re.search(r',\s*pop', low):
                        tail = re.split(r',\s*pop', low, maxsplit=1)[1]
                        regs = [r.strip().strip(',') for r in re.split(r'[\s,]+', tail) if r.strip()]
                        total = sum(reg_bytes(r) for r in regs)
                        if total > 0 and i + total*2 <= n:
                            blob = hex_buffer[i:i + total*2]
                            spaced = ' '.join(blob[j:j+2] for j in range(0, len(blob), 2))
                            output_lines.append(f"hex {spaced}\n")
                            i += total*2
                            state.update_position(total)
                    continue

                if addr in gadgets:
                    line = gadgets[addr].strip()
                    low = line.lower()
                    if low.startswith("sp =") and "pop" in low:
                        output_lines.append(f"{line}\n")
                        continue

                    regs = []
                    if 'pop' in low:
                        tail = re.split(r'\bpop\b', line, 1)[1]
                        toks = [t.strip().strip(',') for t in re.split(r'[\s,]+', tail) if t.strip()]
                        for tok in toks:
                            tok_l = tok.lower().strip(',')
                            if tok_l == 'pc' or tok_l == 'rt':
                                break
                            if re.fullmatch(r'[a-z0-9]+', tok_l):
                                regs.append(tok_l)

                    total = sum(reg_bytes(r) for r in regs) if regs else 0
                    before_pop = ''
                    if 'pop' in low:
                        before_pop = re.split(r'\bpop\b', line, 1)[0].strip()

                    if regs and total > 0:
                        off = 0
                        for idx, r in enumerate(regs):
                            rb = reg_bytes(r)
                            bytes_left = n - i
                            if bytes_left >= rb*2:
                                part = hex_buffer[i:i+rb*2]
                                spaced = ' '.join(part[j:j+2] for j in range(0, len(part), 2))
                                output_lines.append(f"{r} = hex {spaced}\n")
                                i += rb*2
                                state.update_position(rb)
                            else:
                                output_lines.append(f"pop {r}\n")
                        continue

                    if 'pop' in low and before_pop:
                        output_lines.append(f"{line}\n")
                        continue
                    elif 'pop' in low and not before_pop:
                        continue
                    output_lines.append(f"{line}\n")
                    continue

                if addr in disas:
                    lines, new_i = consume_pop_chain_from_disas(addr, disas, hex_buffer, i, state)
                    for L in lines:
                        output_lines.append(f"{L}\n")
                    bytes_consumed = (new_i - i) // 2
                    state.update_position(bytes_consumed)
                    i = new_i
                    continue

                output_lines.append(f"call 0x{addr:X}\n")
                state.update_position(4)

            rem = n - i
            if rem == 4:
                leftover = hex_buffer[i:i+4]
                spaced = ' '.join(leftover[j:j+2] for j in range(0, len(leftover), 2))
                output_lines.append(f"hex {spaced}\n")
                state.update_position(2)
                
    return output_lines