# CHIP-8 interpreter
> CHIP-8 interpreter written using Python language & pygame library.

[![Build Status](https://travis-ci.org/mfurga/chip8.svg?branch=master)](https://travis-ci.org/mfurga/chip8)
[![Coverage Status](https://coveralls.io/repos/github/mfurga/chip8/badge.svg?branch=master)](https://coveralls.io/github/mfurga/chip8?branch=master)
[![License MIT](https://img.shields.io/badge/license-MIT-%237900CA.svg)](https://github.com/mfurga/chip8/blob/master/LICENSE)
[![Python2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)

![CHIP-8 Games](https://raw.githubusercontent.com/mfurga/chip8/master/demo.png)

## Some details
CHIP-8 is an interpreted programming language which was initially used in the late 1970s. It was made to allow more easily programed game for those computers. All programs written in CHIP-8 are run on a virtual machine which interprets each instruction.

### Memory map
Most common implementation of CHIP-8 has 4096 (0x1000) bytes of RAM, starting at location 0x000 (0) to 0xFFF (4095). The first 512 (0x200) bytes are reserved for the CHIP-8 interpreter, in my case this space is used to store fonts data and stack.

```
+----------------+= 0xFFF (4095) End of CHIP-8 RAM
|                |
|                |
|                |
|                |
|                |
| 0x200 to 0xFFF |
| CHIP-8 Program |
|                |
|                |
|                |
|                |
|                |
+----------------+= 0x200 (512) Start of program
|                |
| 0x050 to 0x1FF |
|     Stack      |
|                | 
+----------------+= 0x050 (80) Start of stack 
| 0x000 to 0x049 | 
|     Fonts      |
+----------------+= 0x000 (0) Start of CHIP-8 RAM
```

### Instruction Set Table

| Mnemonic | Opcode | Description |
|----------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| CLS | 00EE | Clear the display. |
| RET | 00EE | Return from a subroutine. |
| JMP | 1nnn | Jump to location nnn. |
| CALL | 2nnn | Execute subroutine starting at address nnn. |
| SE | 3xkk | Skip the following instruction if the value of Vx equals kk. |
| SNE | 4xkk | Skip the following instruction if the value of Vx not equals kk.  |
| SER | 5xy0 | Skip the following instruction if the value of Vx equals Vy. |
| LD | 6xkk | Store the value kk in register Vx. |
| ADD | 7xkk | Add the value kk to the value of register Vx. |
| LDR | 8xy0 | Store the value of register Vy in register Vx. |
| OR | 8xy1 | Store the value of (Vx OR Vy) in register Vx. |
| AND | 8xy2 | Store the value of (Vx AND Vy) in register Vx. |
| XOR | 8xy3 | Store the value of (Vx XOR Vy) in register Vx. |
| ADDR | 8xy4 | Add the value of register Vx to register Vy. Set register VF to 1 if a carry occurs otherwise set to 0. |
| SUB | 8xy5 | Subtract the value of register Vy from register Vx. Set register VF to 1 if a borrow occurs otherwise set to 0. |
| SHR | 8xy6 |  Set register VF to 1 if the least-significant bit of Vx is 1 otherwise set to 0. Store the value of register Vx shifted right by one in register Vx. |
| SUBN | 8xy7 | Subtract the value of register Vx from register Vy. Store result in register Vx. Set register VF to 0 if Vy borrow occurs otherwise set to 1. |
| SHL | 8xyE | Set register VF to 1 if the most-significant bit of Vx is 1 otherwise set to 0 Store the value of register Vx shifted left by one in register Vx. |
| SNER | 9xy0 | Skip the following instruction if value of the register Vx is not equal the value of register Vy. |
| LDI | Annn | Store address nnn in register I. |
| JMPR | Bnnn | Jump to address nnn + V0. |
| RND | Cxkk | Set register Vx to random number ANDed with the value kk. |
| DRW | Dxyn | Draw n-byte sprite starting at memory location I at (Vx, Vy). Set register VF to 1 if any pixels are erased otherwise set to 0. |
| SKP | Ex9E | Skip the following instruction if key with the value of Vx is pressed. |
| SNKP | ExA1 | Skip the following instruction if key with the value of Vx is not pressed. |
| LDT | Fx07 | Store the value of the delay timer in register Vx. |
| LDK | Fx0A | Wait for a keypress and store the value of the key in register Vx. |
| LDDT | Fx15 | Set delay timer to the value of register Vx. |
| LDST | Fx18 | Set sound timer to the value of register Vx. |
| ADDI | Fx1E | Set register I to the value of (I + Vx). |
| LDF | Fx29 | Set register I to the location for sprite corresponding to the value of Vx. |
| LDB | Fx33 | Store BCD representation of Vx in memory at address I, I+1 and I+2. |
| LDIR | Fx55 | Store the values of registers V0 through Vx in memory starting at address I. |
| LDRI | Fx65 | Read registers V0 through Vx from memory starting at address I. |

## Installation / Requirements

- [Python 2.7](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/wiki/GettingStarted)

You can also easly install the require packages using the following command:
```
pip install -r requirements.txt
```

## Usage
Just run `chip8.py` and specify the positional argument which is the CHIP-8 ROM.
```
usage: ./chip8.py [-h] [-d DELAY] [-s SCALE] [-v] program

CHIP-8 interpreter

positional arguments:
  program                  CHIP-8 ROM

optional arguments:
  -h, --help               show this help message and exit
  -d DELAY, --delay DELAY  Specify delay for every instruction (default=1ms)
  -s SCALE, --scale SCALE  Specify scale for width & height (default=10)
  -v, --verbose            Enable verbose output
```

Have fun! :tada:

## License
MIT &copy; Mateusz Furga
