#
# CHIP-8 interpreter.
#
# Copyright (C) 2018 Mateusz Furga
# This software is released under the MIT license.

import pygame
import random

from display import KEY_MAP


class InvalidOpcodeException(Exception):
    def __init__(self, opcode):
        super(InvalidOpcodeException, self).__init__(
            '{:04X} opcode not found.'.format(opcode)
        )


class Opcode(object):
    '''
    CHIP-8 instuctions class.

    Docstrings source:
        http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
    '''
    def __init__(self, vm):
        self.vm = vm

        self.opcodes = {
            0x0: self.execute_clear_or_return_instruction,

            0x1: self.JMP, 0x2: self.CALL, 0x3: self.SE,
            0x4: self.SNE, 0x5: self.SER,  0x6: self.LD,
            0x7: self.ADD,

            0x8: self.execute_bitwise_instruction,

            0x9: self.SNER, 0xA: self.LDI, 0xB: self.JMPR,
            0xC: self.RND,  0xD: self.DRW, 0xE: self.SKP,

            0xF: self.execute_misc_instruction
        }

        self.clear_and_return_instructions_set = {
            0x00E0: self.CLS, 0x00EE: self.RET
        }

        self.bitwise_instruction_set = {
            0x0: self.LDR, 0x1: self.OR,   0x2: self.AND,
            0x3: self.XOR, 0x4: self.ADDR, 0x5: self.SUB,
            0x6: self.SHR, 0x7: self.SUBN, 0xE: self.SHL
        }

        self.misc_instruction_set = {
            0x07: self.LDT,  0x0A: self.LDK,  0x15: self.LDDT,
            0x18: self.LDST, 0x1E: self.ADDI, 0x29: self.LDF,
            0x33: self.LDB,  0x55: self.LDIR, 0x65: self.LDRI
        }

    def execute_clear_or_return_instruction(self):
        '''
        Executes clear or return instruction.
        '''
        try:
            return self.clear_and_return_instructions_set[self.opcode]()
        except KeyError:
            raise InvalidOpcodeException(self.opcode)

    def execute_bitwise_instruction(self):
        '''
        Executes bitwise instructions.
        '''
        try:
            return self.bitwise_instruction_set[self.opcode & 0xf]()
        except KeyError:
            raise InvalidOpcodeException(self.opcode)

    def execute_misc_instruction(self):
        '''
        Executes misc instructions.
        '''
        try:
            return self.misc_instruction_set[self.opcode & 0xff]()
        except KeyError:
            raise InvalidOpcodeException(self.opcode)

    def decrement_registers(self):
        '''
        Decrements sound timer & delay timer registers.
        '''
        if self.vm.dt > 0:
            self.vm.dt -= 1
        if self.vm.st > 0:
            self.vm.st -= 1
            pygame.mixer.music.play(0) if self.vm.st == 0 else None

    def instruction_lookup(self, opcode):
        '''
        Performs instruction using the most significant nibble.
        '''
        self.opcode = opcode
        return self.opcodes[opcode >> 12]()

    def CLS(self):
        '''
        00E0 - CLS
        Clear the display.
        '''
        self.vm.display.clear_display()
        return True

    def RET(self):
        '''
        00EE - RET
        Return from a subroutine.

        The interpreter sets the program counter to the address
        at the top of the stack, then subtracts 1 from the stack pointer.
        '''
        self.vm.sp -= 2
        self.vm.pc = self.vm.mem.fetch_word(self.vm.sp)
        return True

    def JMP(self):
        '''
        1nnn - JP addr
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        '''
        self.vm.pc = self.opcode & 0xfff
        return True

    def CALL(self):
        '''
        2nnn - CALL addr
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current
        PC on the top of the stack. The PC is then set to nnn.
        '''
        self.vm.mem.store_word(self.vm.sp, self.vm.pc)
        self.vm.sp += 2
        self.vm.pc = self.opcode & 0xfff
        return True

    def SE(self):
        '''
        3xkk - SE Vx, byte
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal,
        increments the program counter by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        if self.vm.v[vx] == self.opcode & 0xff:
            self.vm.pc += 2
        return True

    def SNE(self):
        '''
        4xkk - SNE Vx, byte
        Skip next instruction if Vx != kk.

        The interpreter compares register Vx to kk, and if they are not equal,
        increments the program counter by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        if self.vm.v[vx] != self.opcode & 0xff:
            self.vm.pc += 2
        return True

    def SER(self):
        '''
        5xy0 - SE Vx, Vy
        Skip next instruction if Vx = Vy.

        The interpreter compares register Vx to register Vy, and if they are
        equal, increments the program counter by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        if self.vm.v[vx] == self.vm.v[vy]:
            self.vm.pc += 2
        return True

    def LD(self):
        '''
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.v[vx] = self.opcode & 0xff
        return True

    def ADD(self):
        '''
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then
        stores the result in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        byte = self.opcode & 0xff
        self.vm.v[vx] = (self.vm.v[vx] + byte) & 0xff
        return True

    def LDR(self):
        '''
        8xy0 - LD Vx, Vy
        Set Vx = Vy.

        Stores the value of register Vy in register Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[vx] = self.vm.v[vy]
        return True

    def OR(self):
        '''
        8xy1 - OR Vx, Vy
        Set Vx = Vx OR Vy.

        Performs a bitwise OR on the values of Vx and Vy, then stores the
        result in Vx. A bitwise OR compares the corrseponding bits from
        two values, and if either bit is 1, then the same bit in the result
        is also 1. Otherwise, it is 0.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[vx] |= self.vm.v[vy]
        return True

    def AND(self):
        '''
        8xy2 - AND Vx, Vy
        Set Vx = Vx AND Vy.

        Performs a bitwise AND on the values of Vx and Vy, then stores the
        result in Vx. A bitwise AND compares the corrseponding bits from
        two values, and if both bits are 1, then the same bit in the result
        is also 1. Otherwise, it is 0.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[vx] &= self.vm.v[vy]
        return True

    def XOR(self):
        '''
        8xy3 - XOR Vx, Vy
        Set Vx = Vx XOR Vy.

        Performs a bitwise exclusive OR on the values of Vx and Vy, then
        stores the result in Vx.An exclusive OR compares the corrseponding
        bits from two values, and if the bits are not both the same, then
        the corresponding bit in the result is set to 1. Otherwise, it is 0.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[vx] ^= self.vm.v[vy]
        return True

    def ADDR(self):
        '''
        8xy4 - ADD Vx, Vy
        Set Vx = Vx + Vy, set VF = carry.

        The values of Vx and Vy are added together. If the result is greater
        than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0.
        Only the lowest 8 bits of the result are kept, and stored in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[0xf] = 1 if (self.vm.v[vx] + self.vm.v[vy]) > 0xff else 0
        self.vm.v[vx] = (self.vm.v[vx] + self.vm.v[vy]) & 0xff
        return True

    def SUB(self):
        '''
        8xy5 - SUB Vx, Vy
        Set Vx = Vx - Vy, set VF = NOT borrow.

        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted
        from Vx, and the results stored in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[0xf] = 1 if (self.vm.v[vx] > self.vm.v[vy]) else 0
        self.vm.v[vx] = (self.vm.v[vx] - self.vm.v[vy]) & 0xff
        return True

    def SHR(self):
        '''
        8xy6 - SHR Vx {, Vy}
        Set Vx = Vx SHR 1.

        If the least-significant bit of Vx is 1, then VF is set to 1,
        otherwise 0. Then Vx is divided by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[0xf] = self.vm.v[vx] & 0b1
        self.vm.v[vx] >>= 1
        return True

    def SUBN(self):
        '''
        8xy7 - SUBN Vx, Vy
        Set Vx = Vy - Vx, set VF = NOT borrow.

        If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted
        from Vy, and the results stored in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[0xf] = 1 if (self.vm.v[vy] > self.vm.v[vx]) else 0
        self.vm.v[vx] = (self.vm.v[vy] - self.vm.v[vx]) & 0xff
        return True

    def SHL(self):
        '''
        8xyE - SHL Vx {, Vy}
        Set Vx = Vx SHL 1.

        If the most-significant bit of Vx is 1, then VF is set to 1,
        otherwise to 0. Then Vx is multiplied by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        self.vm.v[0xf] = self.vm.v[vx] >> 7
        self.vm.v[vx] = (self.vm.v[vx] << 1) & 0xff
        return True

    def SNER(self):
        '''
        9xy0 - SNE Vx, Vy
        Skip next instruction if Vx != Vy.

        The values of Vx and Vy are compared, and if they are not equal,
        the program counter is increased by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf

        if self.vm.v[vx] != self.vm.v[vy]:
            self.vm.pc += 2
        return True

    def LDI(self):
        '''
        Annn - LD I, addr
        Set I = nnn.

        The value of register I is set to nnn.
        '''
        self.vm.i = self.opcode & 0xfff
        return True

    def JMPR(self):
        '''
        Bnnn - JP V0, addr
        Jump to location nnn + V0.

        The program counter is set to nnn plus the value of V0.
        '''
        self.vm.pc = self.vm.v[0x0] + self.opcode & 0xfff
        return True

    def RND(self):
        '''
        Cxkk - RND Vx, byte
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then
        ANDed with the value kk. The results are stored in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.v[vx] = random.randint(0, 0xff) & self.opcode & 0xff
        return True

    def DRW(self):
        '''
        Dxyn - DRW Vx, Vy, nibble
        Display n-byte sprite starting at memory location I at (Vx, Vy),
        set VF = collision.

        The interpreter reads n bytes from memory, starting at the address
        stored in I. These bytes are then displayed as sprites on screen at
        coordinates (Vx, Vy). Sprites are XORed onto the existing screen.
        If this causes any pixels to be erased, VF is set to 1, otherwise it
        is set to 0. If the sprite is positioned so part of it is outside the
        coordinates of the display, it wraps around to the opposite side of
        the screen.
        '''
        vx = (self.opcode >> 8) & 0xf
        vy = (self.opcode >> 4) & 0xf
        data = self.vm.mem.fetch_many(self.vm.i, self.opcode & 0xf)
        point = (self.vm.v[vx], self.vm.v[vy])

        self.vm.display.draw_sprite(point, data)
        return True

    def SKP(self):
        '''
        Ex9E - SKP Vx or ExA1 - SKNP Vx
        Skip next instruction if key with the value of Vx is (not) pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx
        is currently in the down position, PC is increased by 2.
        '''
        vx = (self.opcode >> 8) & 0xf
        key = pygame.key.get_pressed()

        if self.opcode & 0xff == 0x9E:
            if key[KEY_MAP[self.vm.v[vx]]]:
                self.vm.pc += 2

        elif self.opcode & 0xff == 0xA1:
            if not key[KEY_MAP[self.vm.v[vx]]]:
                self.vm.pc += 2
        return True

    def LDT(self):
        '''
        Fx07 - LD Vx, DT
        Set Vx = delay timer value.

        The value of DT is placed into Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.v[vx] = self.vm.dt & 0xff
        return True

    def LDK(self):
        '''
        Fx0A - LD Vx, K
        Wait for a key press, store the value of the key in Vx.

        All execution stops until a key is pressed, then the value of that
        key is stored in Vx.
        '''
        vx = (self.opcode >> 8) & 0xf

        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_MAP.values():
                    self.vm.v[vx] = KEY_MAP.values().index(event.key)
                    break
        return True

    def LDDT(self):
        '''
        Fx15 - LD DT, Vx
        Set delay timer = Vx.

        DT is set equal to the value of Vx.
        '''
        vx = (self.opcode << 8) & 0xf
        self.vm.dt = self.vm.v[vx]
        return True

    def LDST(self):
        '''
        Fx18 - LD ST, Vx
        Set sound timer = Vx.

        ST is set equal to the value of Vx.
        '''
        vx = (self.opcode << 8) & 0xf
        self.vm.st = self.vm.v[vx]
        return True

    def ADDI(self):
        '''
        Fx1E - ADD I, Vx
        Set I = I + Vx.

        The values of I and Vx are added, and the results are stored in I.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.i = (self.vm.i + self.vm.v[vx]) & 0xffff
        return True

    def LDF(self):
        '''
        Fx29 - LD F, Vx
        Set I = location of sprite for digit Vx.

        The value of I is set to the location for the hexadecimal sprite
        corresponding to the value of Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.i = self.vm.v[vx] * 5
        return True

    def LDB(self):
        '''
        Fx33 - LD B, Vx
        Store BCD representation of Vx in memory locations I, I+1, and I+2.

        The interpreter takes the decimal value of Vx, and places the hundreds
        digit in memory at location in I, the tens digit at location I+1,
        and the ones digit at location I+2.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.mem.store_byte(self.vm.i, self.vm.v[vx] / 100)
        self.vm.mem.store_byte(self.vm.i + 1, (self.vm.v[vx] / 10) % 10)
        self.vm.mem.store_byte(self.vm.i + 2, self.vm.v[vx] % 10)
        return True

    def LDIR(self):
        '''
        Fx55 - LD [I], Vx
        Store registers V0 through Vx in memory starting at location I.

        The interpreter copies the values of registers V0 through Vx into
        memory, starting at the address in I.
        '''
        vx = (self.opcode >> 8) & 0xf
        self.vm.mem.store_many(self.vm.i, self.vm.v[:vx + 1])
        return True

    def LDRI(self):
        '''
        Fx65 - LD Vx, [I]
        Read registers V0 through Vx from memory starting at location I.

        The interpreter reads values from memory starting at location I
        into registers V0 through Vx.
        '''
        vx = (self.opcode >> 8) & 0xf
        data = self.vm.mem.fetch_many(self.vm.i, vx + 1)
        for i, v in enumerate(data):
            self.vm.v[i] = v
        return True
