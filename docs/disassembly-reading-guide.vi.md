# Hướng dẫn đọc Disassembly

Disassembly (disas) là cách biểu diễn mã máy (opcode) dưới dạng dễ đọc hơn với con người. Format cơ bản của nó sẽ là:

```
<Address>    <Opcode>        <Instruction>
```

Với:
- `<Address>`: Địa chỉ của lệnh
- `<Opcode>`: Mã máy
- `<Instruction>`: Lệnh

Ta sẽ lấy ví dụ:

```
1:64E4H	8200			MOV R2, R0
```

Thì ta có:
- Address: `1:64E4H`
- Opcode: `8200`
- Instruction: `MOV R2, R0`
Chức năng của địa chỉ `1:64E4H` sẽ là cho `R2 = R0`. Tuy nhiên ta không thể đoán rằng `1:64E4H` sẽ chỉ cho `R2 = R0` vì vậy ta cần đọc các lệnh ở bên dưới nó nữa.

```
1:64E4H	8200			MOV R2, R0
1:64E6H	F60E			POP R6
1:64E8H	FC1E			POP ER12
1:64EAH	F28E			POP PC
```

Ở đây ta thấy được toàn diện hơn đó là `1:64E4H` thực hiện `r2 = r0`, `pop r6`, `pop er12` và `pop pc` để quay về nơi `1:64E4H` được gọi. Như vậy thì ta đã hiểu được chức năng của `1:64E4H`.

**Tuy nhiên** có một điều rất quan trọng là để có thể đọc hiểu được Instruction thì bạn cần phải hiểu về cấu trúc của bộ xử lý và các register của nó.
Vì vậy bạn cần đọc `nX-U8100 Core Instruction Manual.pdf` và tìm hiểu về ASM để hiểu thêm vấn đề này.