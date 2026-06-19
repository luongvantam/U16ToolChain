#!/usr/bin/env python3
# only fx580vnx
import sys
import argparse

def create_mapping(table, token_mode=False):
    mapping = {}
    for row in range(len(table)):
        for col in range(len(table[row])):
            value = table[row][col]
            key = f"{row*16+col:02X}"
            if token_mode:
                mapping[key] = f"<{key}>" if value == "@" else value
            else:
                mapping[key] = value
    return mapping

def table_token_fx580vnx():
    table = [
        ["<00>", "<01>", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@"],
        ["@", "@", "@", "@", "@", "@", "@", "@", "@", "▯", "@", "@", "@", "@", "@", "@"],
        ["𝒊", "e", "𝜋", ":", "$", "?", "@", "@", "@", "@", "@", "@", ",", "x10", ".", "@"],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "𝗔", "𝗕", "𝗖", "𝗗", "𝗘", "𝗙"],
        ["M","Ans","A","B","C","D","E","F","𝒙","𝒚","PreAns","𝒛","𝜃","@","@","@"],
        ["∑(","∫(","d/d𝒙(","∏(","@","@","@","@","Min(","Max(","Mean(Sum(","@","@","@","@"],
        ["(","P(","Q(","R(","Not(","Neg(","Conjg(","Arg(","Abs(","Rnd(","Det(","Trn(","sinh(","cosh(","tanh(","sinh⁻¹("],
        ["cosh⁻¹(", "tanh⁻¹(", "e^(", "10^(", "√(", "ln(", "³√(", "sin(", "cos(", "tan(", "sin⁻¹(", "cos⁻¹(", "tan⁻¹(", "log(", "Pol(", "Rec("],
        ["@","@","@","Int(","Intg(","Ref(","Rref(","RanInt#(","GCD(","LCM(","RndFix(","@","@","@","@","ReP("],
        ["ImP(", "Identity(", "UnitV(", "Angle(", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@"],
        ["or", "xor", "xnor", "and", "@", "=", "+", "−", "×", "÷", "÷R", "⋅", "∠", "𝗣", "𝗖", "@"],
        ["@", "@", "@", "@", "@", "@", "@", "@", "", "", "₁", "₂", "@", "@", "@", "@"],
        ["-<âm>", "b", "o", "d", "h", "@", "@", "@", "⌟", "^(", "x√(", "@", "@", "@", "@", "@"],
        [")", "▸t", "▸a+b𝒊", "▸r∠𝜃", "⁻¹", "²", "³", "%", "!", "°", "ʳ", "ᵍ", "▫", "𝐄", "𝐏", "𝐓"],
        ["𝐆", "𝐌", "𝐤", "𝐦", "𝝁", "𝐧", "𝐩", "𝐟", "@", "▸Simp ", "@", "@", "@", "@", "@", "@"],
        ["<F0>", "<F1>", "<F2>", "<F3>", "<F4>", "<F5>", "<F6>", "<F7>", "<F8>", "<F9>", "<FA>", "<FB>", "<FC>", "<FD>", "<FE>", "<FF>"],
    ]
    return create_mapping(table, token_mode=True)

def table_char_fx580vnx():
    table = [
        ["##"]*16,
        ["𝒙","𝒚","𝒛","…","▲","▼","▸","₋","$","◁","&","𝑡","ᴛ","ₜ","ₕ","₅"],
        [" ","!",'"',"#","×","%","÷","'","(",")","⋅","+",",","-",".","/"],
        ["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?"],
        ["@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"],
        ["P","Q","R","S","T","U","V","W","X","Y","Z","[","▫","]","^","_"],
        ["−","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"],
        ["p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","├"],
        ["𝒊","𝒆","","","","°","ʳ","ᵍ","∠","","","","","→","∏","⇒"],
        ["","","","⌟","≤","≠","≥","","√","∫","ᴀ","ʙ","ᴄ","ₙ","▶","◀"],
        ["⁰","¹","²","³","⁴","⁵","⁶","⁷","⁸","⁹","","","","₍","₎",""],
        ["₀","₁","₂","","ꜰ","ɴ","ᴘ","","𝗔","𝗕","𝗖","𝗗","𝗘","𝗙","𝗣","▷"],
        ["∑","𝛼","𝛾","𝜀","𝜃","𝜆","𝜇","𝜋","𝜎","𝜙","ℓ","ℏ","▮","▯","₃","＿"],
        ["𝐟","𝐩","𝐧","𝝁","𝐦","𝐤","𝐌","𝐆","𝐓","𝐏","𝐄","𝐹","ₚ","ₑ","ᴊ","ᴋ"],
        ["","","₉","Å","ₘ","ɪ","₄","","","∟","⟲","↻","ⁿ"],
        ["##"]*16,
    ]
    return create_mapping(table, token_mode=False)

def hex2token(hex_codes: str):
    mapping = table_token_fx580vnx()
    s = hex_codes.replace(" ", "").upper()
    result = []
    i = 0
    while i < len(s):
        code = s[i:i+2]
        if code.startswith("F") and i+4 <= len(s):
            result.append(f"<{s[i:i+4]}>")
            i += 4
        else:
            result.append(mapping.get(code, f"<{code}>"))
            i += 2
    return " ".join(result)

def hex2char(hex_codes: str):
    mapping = table_char_fx580vnx()
    s = hex_codes.replace(" ", "").upper()
    result = []
    i = 0
    while i < len(s):
        code = s[i:i+2]
        if code.startswith("F") and i + 4 <= len(s):
            result.append(f"<{s[i:i+4]}>")
            i += 4
        else:
            val = mapping.get(code)
            if not val or val in ["##"]:
                result.append(f"<{code}>")
            else:
                result.append(val)
            i += 2
    return " ".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Casio fx-580VN X Hex to Token/Char Decoder CLI"
    )
    parser.add_argument(
        "hex_codes", 
        nargs="+", 
        help="Hex codes to decode (e.g., '30 31 32' or '303132')"
    )

    args = parser.parse_args()
    # Combine input if passed as separate arguments
    combined_input = "".join(args.hex_codes)

    print("-" * 40)
    print(f"Token : {hex2token(combined_input)}")
    print(f"Char  : {hex2char(combined_input)}")
    print("-" * 40)

if __name__ == "__main__":
    main()