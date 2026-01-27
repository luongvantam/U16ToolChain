# Guide to Reading Disassembly

Disassembly (disas) is a way of representing machine code (opcode) in a more readable form for humans. Its basic format is:

```
<Address> <Opcode> <Instruction>
```

Where:
- `<Address>`: Address of the instruction
- `<Opcode>`: Machine code
- `<Instruction>`: Instruction

Let's take an example:

```
1:64E4H 8200 MOV R2, R0
```

Then we have:
- Address: `1:64E4H`
- Opcode: `8200`
- Instruction: `MOV R2, R0`
The function of the address `1:64E4H` is to make `R2 = R0`. However, we cannot assume that `1:64E4H` will simply mean `R2 = R0`, so we need to read the instructions below it as well.

```
1:64E4H 8200 MOV R2, R0
1:64E6H F60E POP R6
1:64E8H FC1E POP ER12
1:64EAH F28E POP PC
```

Here we see a more comprehensive picture: `1:64E4H` executes `r2 = r0`, `pop r6`, `pop er12`, and `pop pc` to return to where `1:64E4H` was called. Thus, we understand the function of `1:64E4H`.

**However**, it is very important to understand the structure of the processor and its registers in order to read and understand the instructions.
Therefore, you need to read the `nX-U8100 Core Instruction Manual.pdf` and learn about ASM to better understand this issue.