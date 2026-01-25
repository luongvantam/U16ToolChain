org 0xE9E0

setlr
reset_sfr
DI,RT
buffer_clear
xr0 = hex 0a 01 36 ed
smallprint
xr0 = hex 58 0f 08 08
render_bitmap
er0 = hex 50 da
xr0 = hex b0 01 08 14
render_bitmap
er0 = hex c2 da
xr0 = hex b0 2b 08 14
setlr
render_bitmap
er0 = hex c2 da
render.ddd4
er0 = hex 98 d7
getkey
er0 = hex 00 00
ea = hex 92 da
ea_switchcase
er6 = [ea+]
sp = er6,pop er8
xr0 = hex 1e da 38 d3
calc_func
setlr
xr0 = hex 44 ed e0 d7
[er0] = er2,rt
er14 = hex e0 d7
sp = er14,pop er14
setlr
xr0 = hex 44 ed aa d7
[er0] = er2,rt
xr0 = hex 20 da 38 d3
calc_func
xr0 = hex 22 da 2e d3
calc_func
setlr
ea = hex 9a da
er2 = hex 00 ea
er0 = [er2],r2 = 9,rt
ea_switchcase
er6 = [ea+]
sp = er6,pop er8
setlr
ea = hex a6 da
er2 = hex 12 ea
er0 = [er2],r2 = 9,rt
ea_switchcase
er6 = [ea+]
sp = er6,pop er8
xr0 = hex 26 da 42 d3
calc_func
er6 = hex c0 d9
sp = er6,pop er8
setlr
er2 = hex 00 ea
er0 = [er2],r2 = 9,rt
r0 = 0
er2 = hex 00 14
er0 - er2_gt,r0 = 0|r0 = 1,rt
er4 = hex 86 d8
er2 = hex 42 00
er0 *= r2,er2 = er0,er0 += er4,rt
xr0 = hex 30 30 30 30
sp = er14,pop er14
setlr
er2 = hex 00 ea
er0 = [er2],r2 = 9,rt
r0 = 0
er2 = hex 00 23
er2 - er0_gt,r0 = 0|r0 = 1,rt
er4 = hex be d8
er2 = hex 0a 00
er0 *= r2,er2 = er0,er0 += er4,rt
xr0 = hex 30 30 30 30
sp = er14,pop er14
er6 = hex c0 d9
sp = er6,pop er8
xr0 = hex 13 d1 01 00
[er0] = r2
xr0 = hex 2a da 2e d3
calc_func
xr0 = hex 42 d3 00 00
num_fromdigit
xr0 = hex 28 da 38 d3
calc_func
buffer_clear
xr0 = hex 0e 01 58 da
smallprint
xr0 = hex 0e 11 86 da
smallprint
xr0 = hex 0e 21 62 da
smallprint
xr0 = hex 0e 31 74 da
smallprint
render.ddd4
waitshift_blank
xr0 = hex 24 da 00 e5
calc_func
er0 = hex 00 e5
num_to_byte
er2 = hex 15 ea
[er2] = r0,r2 = 0
er2 = hex 17 eb
[er2] = r0,r2 = 0
setlr
r1 = 0,rt
er2 = hex 0e 00
er0 += er2,rt
er2 = hex 4f eb
[er2] = r0,r2 = 0
er2 = hex 08 00
er0 += er2,rt
er2 = hex 25 ea
[er2] = r0,r2 = 0
er2 = er0,er0 += er4,rt
er0 = hex 3f 00
er0 -= er2,rt
er2 = hex 27 ea
[er2] = r0,r2 = 0
er0 = hex b0 00
er2 = hex 12 ea
[er2] = r0,r2 = 0
er2 = hex 24 ea
[er2] = r0,r2 = 0
xr0 = hex 42 d3 3c ed
num_to_str
setlr
er0 = hex 2e d3
num_to_byte
er2 = hex 01 ea
[er2] = r0,r2 = 0
er2 = hex ff ff
er8 = hex 12 ea
xr8 = hex 24 ea 30 30
er2 = hex ff ff
xr8 = hex 30 30 30 30
xr0 = hex 30 d6 84 d1
BL strcpy
er14 = hex 2e d6
sp = er14,pop er14
hex 2C DA 32 DA 3A DA 48 DA 44 DA 3E DA 40 DA A7 31 2E 38 00 00 43 A6 30 2E 30 39 00 00 42 A6 43 00 30 00 32 37 00 00 44 A6 31 00 87 31 30 2C 33 31 D0 00 3C 7E FF FF FF FF 7E 3C 47 61 6D 65 20 4F 76 65 72 00 53 68 69 66 74 20 74 6F 20 72 65 73 74 61 72 74 20 00 44 65 76 3A 20 4D 69 6E 68 43 61 73 69 6F 6B 31 32 00 53 63 6F 72 65 3A 30 00 00 00 00 00 80 04 AA D7 00 00 D0 D7 58 02 C8 D8 58 38 C8 D8 00 00 18 D8 01 01 34 D9 60 01 4E D8 5E 01 4E D8 5C 01 4E D8 5A 01 4E D8 48 01 38 D8 00 00 C0 D9 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
