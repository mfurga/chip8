[org 0x0]

;;;;;;;;;;;;;; R E G I S T E R S ;;;;;;;;;;;;;;

%define v0 0
%define v1 1
%define v2 2
%define v3 3
%define v4 4
%define v5 5
%define v6 6
%define v7 7
%define v8 8
%define v9 9
%define v10 10
%define v11 11
%define v12 12
%define v13 13
%define v14 14
%define v15 15

;;;;;;;;;;;;;;; O P C O D E S ;;;;;;;;;;;;;;;

; 00E0 - CLS
%macro cls 0
db 0x00, 0xe0
%endmacro

; 00EE - RET
%macro ret 0
db 0x00, 0xee
%endmacro

; 1nnn - JP addr
%macro jmp 1
db (%1 >> 8) & 0xf | 0x1 << 4, %1 & 0xff  ; TODO: Use labels
%endmacro

; 2nnn - CALL addr
%macro call 1
db (%1 >> 8) & 0xf | 0x2 << 4, %1 & 0xff  ; TODO: Use labels
%endmacro

; 3xkk - SE Vx, byte
%macro se 2
db (%1 & 0xf) | 0x3 << 4, %2 & 0xff
%endmacro

; 4xkk - SNE Vx, byte
%macro sne 2
db (%1 & 0xf) | 0x4 << 4, %2 & 0xff
%endmacro

; 5xy0 - SE Vx, Vy
%macro ser 2
db (%1 & 0xf) | 0x5 << 4, (%2 & 0xf) << 4
%endmacro

; 6xkk - LD Vx, byte
%macro ld 2
db (%1 & 0xf) | 0x6 << 4, %2 & 0xff
%endmacro

; 7xkk - ADD Vx, byte
%macro add 2
db (%1 & 0xf) | 0x7 << 4, %2 & 0xff
%endmacro

; 8xy0 - LD Vx, Vy
%macro ldr 2
db (%1 & 0xf) | 0x8 << 4, (%2 & 0xf) << 4
%endmacro

; 8xy1 - OR Vx, Vy
%macro or 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 1
%endmacro

; 8xy2 - AND Vx, Vy
%macro and 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 2
%endmacro

; 8xy3 - XOR Vx, Vy
%macro xor 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 3
%endmacro

; 8xy4 - ADD Vx, Vy
%macro addr 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 4
%endmacro

; 8xy5 - SUB Vx, Vy
%macro sub 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 5
%endmacro

; 8xy6 - SHR Vx {, Vy}
%macro shr 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 6
%endmacro

; 8xy7 - SUBN Vx, Vy
%macro subn 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 7
%endmacro

; 8xyE - SHL Vx {, Vy}
%macro shl 2
db (%1 & 0xf) | 0x8 << 4, ((%2 & 0xf) << 4) | 0xe
%endmacro

; 9xy0 - SNE Vx, Vy
%macro sner 2
db (%1 & 0xf) | 0x9 << 4, (%2 & 0xf) << 4
%endmacro

; Annn - LD I, addr
%macro ldi 1
db (%1 >> 8) & 0xf | 0xa << 4, %1 & 0xff
%endmacro

; Bnnn - JP V0, addr
%macro jmpr 1
db (%1 >> 8) & 0xf | 0xb << 4, %1 & 0xff
%endmacro

; Cxkk - RND Vx, byte
%macro rnd 2
db (%1 & 0xf) | 0xc << 4, %2 & 0xff
%endmacro

; Dxyn - DRW Vx, Vy, nibble
%macro drw 3
db (%1 & 0xf) | 0xd << 4, (%2 & 0xf) << 4 | (%3 & 0xf)
%endmacro

; Ex9E - SKP Vx
%macro skp 1
db (%1 & 0xf) | 0xe << 4, 0x9e
%endmacro

; ExA1 - SKNP Vx
%macro sknp 1
db (%1 & 0xf) | 0xe << 4, 0xa1
%endmacro

; Fx07 - LD Vx, DT
%macro ldt 1
db (%1 & 0xf) | 0xf << 4, 0x07
%endmacro

; Fx0A - LD Vx, K
%macro ldk 1
db (%1 & 0xf) | 0xf << 4, 0x0a
%endmacro

; Fx15 - LD DT, Vx
%macro lddt 1
db (%1 & 0xf) | 0xf << 4, 0x15
%endmacro

; Fx18 - LD ST, Vx
%macro ldst 1
db (%1 & 0xf) | 0xf << 4, 0x18
%endmacro

; Fx1E - ADD I, Vx
%macro addi 1
db (%1 & 0xf) | 0xf << 4, 0x1e
%endmacro

; Fx29 - LD F, Vx
%macro ldf 1
db (%1 & 0xf) | 0xf << 4, 0x29
%endmacro

; Fx33 - LD B, Vx
%macro ldb 1
db (%1 & 0xf) | 0xf << 4, 0x33
%endmacro

; Fx55 - LD [I], Vx
%macro ldir 1
db (%1 & 0xf) | 0xf << 4, 0x55
%endmacro

; Fx65 - LD Vx, [I]
%macro ldri 1
db (%1 & 0xf) | 0xf << 4, 0x65
%endmacro
