org 0xe9e0

restore:
    xr0 = 0xD830, adr_of home
    BL memcpy,pop er0
    0x0101

display:
	setlr
	DI,RT
	er0 = 0x0000
	er2 = 0x0000
	BL memset,pop er2
	0x0000
	qr0 = 0x25, 0x16, 0x80, 0x16, 0x30303030
	call 0x09846
	0x646E
	call 0x0947e
	
matrix:
	xr0 = 0xF034, 0x3F, 0x30
	[er0] = r2
	
setup:
    er2 = 0x0000
    er0 = 0xF038
    [er0] = er2,rt

home:
    er2 = 0x0100
    er8 = 0xF038
    [er8]+=er2,pop xr8
    0x30303030

delay:
	er0 = 0x0101
	BL delay,pop xr0
	0x30303030
	
loop:
    xr0 = adr_of length, 0x0101
    [er0] = er2,rt
    xr0 = adr_of home, 0xD830
    BL memcpy,pop er0
    
length:
    0x0101
    
set_sp:
    er6 = adr_of [-2] home
    sp = er6,pop er8