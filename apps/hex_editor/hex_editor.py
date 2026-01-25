#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, IntVar, BooleanVar
from pathlib import Path

BYTES_PER_LINE = 16

class HexEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Hex Editor')
        self.geometry('1000x650')
        self._filepath = None
        self._data = bytearray()
        self._cursor_offset = 0
        self._dark_mode = True
        self._font_size = IntVar(value=11)
        self._autosave = BooleanVar(value=False)
        self._nibble_state = ''

        self._make_ui()
        self.apply_theme()

    def _make_ui(self):
        self.top = tk.Frame(self)
        self.top.pack(fill='x', pady=5)

        tk.Button(self.top, text='Open', command=self.open_file).pack(side='left', padx=3)
        tk.Button(self.top, text='Save', command=self.save_file).pack(side='left', padx=3)
        tk.Button(self.top, text='Close File', command=self.close_file).pack(side='left', padx=3)
        tk.Button(self.top, text='Reload', command=self.reload_file).pack(side='left', padx=3)
        tk.Button(self.top, text='Settings', command=self.open_settings).pack(side='left', padx=3)

        tk.Label(self.top, text='Go to addr:').pack(side='left', padx=3)
        self.goto_entry = tk.Entry(self.top, width=10)
        self.goto_entry.pack(side='left')
        tk.Button(self.top, text='Go', command=self.goto_address).pack(side='left', padx=3)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True)
        self.text = tk.Text(self.body, font=('Courier', self._font_size.get()), wrap='none', undo=True)
        self.text.pack(side='left', fill='both', expand=True)
        vsb = tk.Scrollbar(self.body, orient='vertical', command=self.text.yview)
        vsb.pack(side='right', fill='y')
        self.text['yscrollcommand'] = vsb.set

        self.text.bind('<Button-1>', self.on_click)
        self.text.bind('<Key>', self.on_key)

        self.text.tag_configure('highlight', background='#2E86C1', foreground='white')
        self.text.tag_configure('hexzone', foreground='#E67E22')
        self.text.tag_configure('asciizone', foreground='#1E8449')

        self.status = tk.Label(self, text='No file loaded', anchor='w')
        self.status.pack(fill='x')

    def apply_theme(self):
        dark = self._dark_mode
        colors = {'bg': '#121212', 'fg': '#E0E0E0', 'btn_bg': '#2C2C2C', 'btn_fg': 'white', 'entry_bg': '#2E2E2E', 'entry_fg': 'white'} if dark else {'bg': 'white', 'fg': 'black', 'btn_bg': '#E8E8E8', 'btn_fg': 'black', 'entry_bg': 'white', 'entry_fg': 'black'}

        self.configure(bg=colors['bg'])
        self.top.configure(bg=colors['bg'])
        self.body.configure(bg=colors['bg'])
        self.text.configure(bg=colors['bg'], fg=colors['fg'], insertbackground=colors['fg'], font=('Courier', self._font_size.get()))
        self.status.configure(bg=colors['bg'], fg=colors['fg'])

        for w in self.top.winfo_children():
            if isinstance(w, tk.Button):
                w.configure(bg=colors['btn_bg'], fg=colors['btn_fg'], activebackground=colors['btn_bg'], activeforeground=colors['fg'])
            elif isinstance(w, tk.Label):
                w.configure(bg=colors['bg'], fg=colors['fg'])
            elif isinstance(w, tk.Entry):
                w.configure(bg=colors['entry_bg'], fg=colors['entry_fg'], insertbackground=colors['fg'])

    def open_settings(self):
        win = Toplevel(self)
        win.title('Settings')
        win.geometry('320x240')
        win.configure(bg='#222' if self._dark_mode else 'white')
        fg_color = 'white' if self._dark_mode else 'black'

        tk.Label(win, text='Appearance', font=('Segoe UI', 11, 'bold'), bg=win['bg'], fg=fg_color).pack(pady=5)
        tk.Button(win, text=('Dark Mode' if not self._dark_mode else 'Light Mode'), command=lambda: self.toggle_theme(win)).pack(pady=3)

        tk.Label(win, text='Font Size:', bg=win['bg'], fg=fg_color).pack(pady=5)
        tk.Scale(win, from_=8, to=18, orient='horizontal', variable=self._font_size, command=lambda _: self.update_font(), bg=win['bg'], fg=fg_color, highlightthickness=0).pack()

        tk.Checkbutton(win, text='Enable AutoSave', variable=self._autosave, bg=win['bg'], fg=fg_color, selectcolor=win['bg']).pack(pady=5)
        tk.Button(win, text='Close', command=win.destroy).pack(pady=10)

    def toggle_theme(self, win):
        self._dark_mode = not self._dark_mode
        self.apply_theme()
        self._render()
        win.destroy()

    def update_font(self):
        self.text.configure(font=('Courier', self._font_size.get()))
        self._render()

    def open_file(self):
        p = filedialog.askopenfilename(title='Open binary file', filetypes=[('All files', '*.*')])
        if not p:
            return
        self._filepath = Path(p)
        try:
            self._data = bytearray(self._filepath.read_bytes())
            self._cursor_offset = 0
            self._render()
            self.status.config(text=f'Loaded: {self._filepath} ({len(self._data)} bytes)')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to open file:\n{e}')

    def save_file(self):
        if not self._filepath:
            return
        try:
            self._filepath.write_bytes(self._data)
            messagebox.showinfo('Saved', f'Saved {len(self._data)} bytes to {self._filepath}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save file:\n{e}')

    def close_file(self):
        self._filepath = None
        self._data.clear()
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.config(state='disabled')
        self._cursor_offset = 0
        self.status.config(text='File closed')

    def reload_file(self):
        if not self._filepath:
            return
        self._data = bytearray(self._filepath.read_bytes())
        self._render()

    def _render(self):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        for base in range(0, len(self._data), BYTES_PER_LINE):
            chunk = self._data[base:base+BYTES_PER_LINE]
            hex_bytes = ' '.join(f'{b:02X}' for b in chunk)
            pad = '   ' * (BYTES_PER_LINE - len(chunk))
            ascii_repr = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            self.text.insert('end', f'{base:08X}  ')
            self.text.insert('end', f'{hex_bytes}{pad}  ', ('hexzone',))
            self.text.insert('end', f'|{ascii_repr}|\n', ('asciizone',))
        self.text.config(state='disabled')
        self._highlight_cursor()
        self.apply_theme()

    def _highlight_cursor(self):
        self.text.tag_remove('highlight', '1.0', 'end')
        if not self._data:
            return
        off = max(0, min(self._cursor_offset, len(self._data)-1))
        line = off // BYTES_PER_LINE
        byte_in_line = off % BYTES_PER_LINE
        start = f'{line+1}.10+{byte_in_line*3}c'
        end = f'{line+1}.10+{byte_in_line*3+2}c'
        try:
            self.text.tag_add('highlight', start, end)
            self.text.see(f'{line+1}.0')
        except tk.TclError:
            pass
        self.status.config(text=f'Cursor at 0x{off:X} ({off})')

    def on_click(self, event):
        idx = self.text.index(f'@{event.x},{event.y}')
        line, col = map(int, idx.split('.'))
        if col < 10 or line <= 0:
            return
        rel = col - 10
        byte_index = rel // 3
        if not (0 <= byte_index < BYTES_PER_LINE):
            return
        off = (line - 1) * BYTES_PER_LINE + byte_index
        if off >= len(self._data):
            return
        self._cursor_offset = off
        self._highlight_cursor()

    def on_key(self, event):
        if not self._data:
            return
        if event.keysym in ('Left', 'Right', 'Up', 'Down'):
            self._move_cursor(event.keysym)
            return 'break'
        ch = event.char.upper()
        if ch in '0123456789ABCDEF':
            self._nibble_state += ch
            if len(self._nibble_state) == 2:
                try:
                    new_val = int(self._nibble_state, 16)
                    self._data[self._cursor_offset] = new_val
                    self._cursor_offset = min(self._cursor_offset + 1, len(self._data)-1)
                    self._nibble_state = ''
                    if self._autosave.get() and self._filepath:
                        self._filepath.write_bytes(self._data)
                    self._render()
                except Exception:
                    self._nibble_state = ''
            self._highlight_cursor()
            return 'break'

    def _move_cursor(self, direction):
        off = self._cursor_offset
        if direction == 'Left': off -= 1
        elif direction == 'Right': off += 1
        elif direction == 'Up': off -= BYTES_PER_LINE
        elif direction == 'Down': off += BYTES_PER_LINE
        self._cursor_offset = max(0, min(off, len(self._data)-1))
        self._highlight_cursor()

    def goto_address(self):
        val = self.goto_entry.get().strip()
        if not val:
            return
        try:
            addr = int(val, 16)
        except ValueError:
            messagebox.showerror('Error', 'Invalid hex address')
            return
        if not (0 <= addr < len(self._data)):
            messagebox.showwarning('Out of range', 'Address exceeds file size')
            return
        self._cursor_offset = addr
        self._highlight_cursor()

if __name__ == '__main__':
    app = HexEditorApp()
    app.mainloop()