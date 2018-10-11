'''
    CHIP-8 emulator.

    Copyright (C) 2018 Mateusz Furga
    This software is released under the MIT license.
'''

import unittest

from chip8.opcode import InvalidOpcodeException, Opcode
from chip8.chip8 import Chip8


class TestOpcode(unittest.TestCase):

    def setUp(self):
        self.vm_opcode = Opcode(Chip8([]))

    def test_ret_instruction(self):
        '''
        00EE - RET
        Return from a subroutine.
        '''
        # Sets stack pointer to n >= 2
        self.vm_opcode.vm.sp = 2

        sp_addr = self.vm_opcode.vm.sp
        self.vm_opcode.instruction_lookup(0x00EE)

        self.assertEqual(self.vm_opcode.vm.sp, sp_addr - 2)

        self.assertEqual(
            self.vm_opcode.vm.pc,
            self.vm_opcode.vm.mem.fetch_word(self.vm_opcode.vm.sp)
        )

    def test_jmp_instruction(self):
        '''
        1nnn - JP addr
        Jump to location nnn.
        '''
        self.vm_opcode.instruction_lookup(0x1FFF)
        self.assertEqual(self.vm_opcode.vm.pc, 0xFFF)

        self.vm_opcode.instruction_lookup(0x1000)
        self.assertEqual(self.vm_opcode.vm.pc, 0x0)

    def test_call_instruction(self):
        '''
        2nnn - CALL addr
        Call subroutine at nnn.
        '''
        self.vm_opcode.vm.pc = 0xddd

        sp_addr = self.vm_opcode.vm.sp
        pc_addr = self.vm_opcode.vm.pc
        self.vm_opcode.instruction_lookup(0x2fff)

        self.assertEqual(self.vm_opcode.vm.sp, sp_addr + 2)
        self.assertEqual(self.vm_opcode.vm.pc, 0xfff)
        self.assertEqual(self.vm_opcode.vm.mem.fetch_word(sp_addr), pc_addr)

    def test_se_instruction(self):
        '''
        3xkk - SE Vx, byte
        Skip next instruction if Vx = kk.
        '''
        pc = self.vm_opcode.vm.pc

        self.vm_opcode.instruction_lookup(0x31ff)
        self.assertEqual(self.vm_opcode.vm.pc, pc)

        self.vm_opcode.vm.v[0xf] = 0xff
        self.vm_opcode.instruction_lookup(0x3fff)
        self.assertEqual(self.vm_opcode.vm.pc, pc + 2)

    def test_sne_instruction(self):
        '''
        4xkk - SNE Vx, byte
        Skip next instruction if Vx != kk.
        '''
        pc = self.vm_opcode.vm.pc

        self.vm_opcode.vm.v[0x0] = 0x00
        self.vm_opcode.instruction_lookup(0x4000)
        self.assertEqual(self.vm_opcode.vm.pc, pc)

        self.vm_opcode.instruction_lookup(0x41ff)
        self.assertEqual(self.vm_opcode.vm.pc, pc + 2)

    def test_ser_instruction(self):
        '''
        5xy0 - SE Vx, Vy
        Skip next instruction if Vx = Vy.
        '''
        pc = self.vm_opcode.vm.pc

        self.vm_opcode.vm.v[0xa] = 1
        self.vm_opcode.vm.v[0xb] = 0
        self.vm_opcode.instruction_lookup(0x5ab0)
        self.assertEqual(self.vm_opcode.vm.pc, pc)

        self.vm_opcode.instruction_lookup(0x5010)
        self.assertEqual(self.vm_opcode.vm.pc, pc + 2)

    def test_ld_instruction(self):
        '''
        6xkk - LD Vx, byte
        Set Vx = kk.
        '''
        self.vm_opcode.instruction_lookup(0x61ff)
        self.assertEqual(self.vm_opcode.vm.v[0x1], 0xff)

    def test_add_instruction(self):
        '''
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.
        '''
        self.vm_opcode.vm.v[0x0] = 0
        self.vm_opcode.instruction_lookup(0x70aa)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xaa)

        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.instruction_lookup(0x70ff)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xfe)

    def test_ldr_instruction(self):
        '''
        8xy0 - LD Vx, Vy
        Set Vx = Vy.
        '''
        self.vm_opcode.vm.v[0x0] = 1

        self.vm_opcode.instruction_lookup(0x8100)
        self.assertEqual(self.vm_opcode.vm.v[0x1], 1)

    def test_or_instruction(self):
        '''
        8xy1 - OR Vx, Vy
        Set Vx = Vx OR Vy.
        '''
        self.vm_opcode.vm.v[0x0] = 0xab
        self.vm_opcode.vm.v[0x1] = 0xff

        self.vm_opcode.instruction_lookup(0x8011)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xff)

    def test_and_instruction(self):
        '''
        8xy2 - AND Vx, Vy
        Set Vx = Vx AND Vy.
        '''
        self.vm_opcode.vm.v[0x0] = 0xab
        self.vm_opcode.vm.v[0x1] = 0x0f

        self.vm_opcode.instruction_lookup(0x8012)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0x0b)

    def test_xor_instruction(self):
        '''
        8xy3 - XOR Vx, Vy
        Set Vx = Vx XOR Vy.
        '''
        self.vm_opcode.vm.v[0x0] = 0xab
        self.vm_opcode.vm.v[0x1] = 0xcc

        self.vm_opcode.instruction_lookup(0x8013)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0x67)

    def test_addr_instruction(self):
        '''
        8xy4 - ADD Vx, Vy
        Set Vx = Vx + Vy, set VF = carry.
        '''
        self.vm_opcode.vm.v[0x0] = 0xaa
        self.vm_opcode.vm.v[0x1] = 0x11

        self.vm_opcode.instruction_lookup(0x8014)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xbb)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 0)

        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.vm.v[0x1] = 0x01

        self.vm_opcode.instruction_lookup(0x8014)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0x00)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 1)

    def test_sub_instruction(self):
        '''
        8xy5 - SUB Vx, Vy
        Set Vx = Vx - Vy, set VF = NOT borrow.
        '''
        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.vm.v[0x1] = 0x10

        self.vm_opcode.instruction_lookup(0x8015)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xef)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 1)

        self.vm_opcode.vm.v[0x0] = 0x10
        self.vm_opcode.vm.v[0x1] = 0x11

        self.vm_opcode.instruction_lookup(0x8015)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xff)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 0)

    def test_shr_instruction(self):
        '''
        8xy6 - SHR Vx {, Vy}
        Set Vx = Vx SHR 1.
        '''
        self.vm_opcode.vm.v[0x0] = 17

        self.vm_opcode.instruction_lookup(0x8016)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 8)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 1)

        self.vm_opcode.vm.v[0x0] = 16

        self.vm_opcode.instruction_lookup(0x8016)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 8)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 0)

    def test_subn_instruction(self):
        '''
        8xy7 - SUBN Vx, Vy
        Set Vx = Vy - Vx, set VF = NOT borrow.
        '''
        self.vm_opcode.vm.v[0x0] = 0x10
        self.vm_opcode.vm.v[0x1] = 0xff

        self.vm_opcode.instruction_lookup(0x8017)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xef)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 1)

        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.vm.v[0x1] = 0x10

        self.vm_opcode.instruction_lookup(0x8017)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0x11)
        self.assertEqual(self.vm_opcode.vm.v[0xf], 0)

    def test_shl_instruction(self):
        '''
        8xyE - SHL Vx {, Vy}
        Set Vx = Vx SHL 1.
        '''
        self.vm_opcode.vm.v[0x0] = 0xff

        self.vm_opcode.instruction_lookup(0x800E)
        self.assertEqual(self.vm_opcode.vm.v[0x0], (0xff << 1) & 0xff)

    def test_sner_instruction(self):
        '''
        9xy0 - SNE Vx, Vy
        Skip next instruction if Vx != Vy.
        '''
        pc = self.vm_opcode.vm.pc
        self.vm_opcode.vm.v[0x0] = 0
        self.vm_opcode.vm.v[0x1] = 0

        self.vm_opcode.instruction_lookup(0x9100)
        self.assertEqual(self.vm_opcode.vm.pc, pc)

        self.vm_opcode.vm.v[0x1] = 1
        self.vm_opcode.instruction_lookup(0x9100)
        self.assertEqual(self.vm_opcode.vm.pc, pc + 2)

    def test_ldi_instruction(self):
        '''
        Annn - LD I, addr
        Set I = nnn.
        '''
        self.vm_opcode.instruction_lookup(0xAABC)
        self.assertEqual(self.vm_opcode.vm.i, 0xABC)

    def test_jmpr_instruction(self):
        '''
        Bnnn - JP V0, addr
        Jump to location nnn + V0.
        '''
        self.vm_opcode.vm.v[0x0] = 0x10
        self.vm_opcode.instruction_lookup(0xB100)
        self.assertEqual(self.vm_opcode.vm.pc, 0x10 + 0x100)

    def test_rnd_instruction(self):
        '''
        Cxkk - RND Vx, byte
        Set Vx = random byte AND kk.
        '''
        self.vm_opcode.instruction_lookup(0xC1FF)
        self.assertIn(self.vm_opcode.vm.v[1], xrange(0, 0xff + 1))

    def test_drw_instruction(self):
        '''
        Dxyn - DRW Vx, Vy, nibble
        Display n-byte sprite starting at memory location I at (Vx, Vy),
        set VF = collision.
        '''
        pass

    def test_skp_instruction(self):
        '''
        Ex9E - SKP Vx or ExA1 - SKNP Vx
        Skip next instruction if key with the value of Vx is (not) pressed.
        '''
        pass

    def test_ldt_instruction(self):
        '''
        Fx07 - LD Vx, DT
        Set Vx = delay timer value.
        '''
        self.vm_opcode.vm.dt = 0xff
        self.vm_opcode.instruction_lookup(0xF007)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xff)

        self.vm_opcode.vm.dt = 0xddd
        self.vm_opcode.instruction_lookup(0xF007)
        self.assertEqual(self.vm_opcode.vm.v[0x0], 0xdd)

    def test_ldk_instruction(self):
        '''
        Fx0A - LD Vx, K
        Wait for a key press, store the value of the key in Vx.
        '''
        pass

    def test_lddt_instruction(self):
        '''
        Fx15 - LD DT, Vx
        Set delay timer = Vx.
        '''
        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.instruction_lookup(0xF015)
        self.assertEqual(self.vm_opcode.vm.dt, 0xff)

    def test_ldst_instruction(self):
        '''
        Fx18 - LD ST, Vx
        Set sound timer = Vx.
        '''
        self.vm_opcode.vm.v[0x0] = 0xff
        self.vm_opcode.instruction_lookup(0xF018)
        self.assertEqual(self.vm_opcode.vm.st, 0xff)

    def test_addi_instruction(self):
        '''
        Fx1E - ADD I, Vx
        Set I = I + Vx.
        '''
        self.vm_opcode.vm.v[0] = 10
        self.vm_opcode.vm.i = 10

        self.vm_opcode.instruction_lookup(0xF01E)
        self.assertEqual(self.vm_opcode.vm.i, 20)

        self.vm_opcode.vm.v[0] = 0xff
        self.vm_opcode.vm.i = 0xffff

        self.vm_opcode.instruction_lookup(0xF01E)
        self.assertEqual(self.vm_opcode.vm.i, 0xFE)

    def test_ldf_instruction(self):
        '''
        Fx29 - LD F, Vx
        Set I = location of sprite for digit Vx.
        '''
        self.vm_opcode.vm.v[0x0] = 1
        self.vm_opcode.instruction_lookup(0xF029)
        self.assertEqual(self.vm_opcode.vm.i, 5)

    def test_ldb_instruction(self):
        '''
        Fx33 - LD B, Vx
        Store BCD representation of Vx in memory locations I, I+1, and I+2.
        '''
        self.vm_opcode.i = 0x0
        self.vm_opcode.vm.v[0x0] = 255
        self.vm_opcode.instruction_lookup(0xF033)

        self.assertEqual(self.vm_opcode.vm.mem.fetch_byte(0x0), 2)
        self.assertEqual(self.vm_opcode.vm.mem.fetch_byte(0x1), 5)
        self.assertEqual(self.vm_opcode.vm.mem.fetch_byte(0x2), 5)

    def test_ldir_instruction(self):
        '''
        Fx55 - LD [I], Vx
        Store registers V0 through Vx in memory starting at location I.
        '''
        self.vm_opcode.vm.i = 0x100
        for i in xrange(len(self.vm_opcode.vm.v)):
            self.vm_opcode.vm.v[i] = i

        self.vm_opcode.instruction_lookup(0xFF55)
        for i in xrange(len(self.vm_opcode.vm.v)):
            self.assertEqual(self.vm_opcode.vm.mem.fetch_byte(0x100 + i), i)

        self.vm_opcode.vm.v[0x0] = 100
        self.vm_opcode.vm.v[0x1] = 101
        self.vm_opcode.vm.v[0x2] = 102
        self.vm_opcode.instruction_lookup(0xF255)
        for i in xrange(len(self.vm_opcode.vm.v[:2]) + 1):
            self.assertEqual(
                self.vm_opcode.vm.mem.fetch_byte(0x100 + i), 100 + i)

        self.assertEqual(self.vm_opcode.vm.v[0x3], 3)

    def test_ldri_instruction(self):
        '''
        Fx65 - LD Vx, [I]
        Read registers V0 through Vx from memory starting at location I.
        '''
        self.vm_opcode.vm.i = 0x100
        self.vm_opcode.vm.mem.store_many(0x100, [0x10, 0x11, 0x12])

        self.vm_opcode.instruction_lookup(0xF265)

        for i in xrange(len(self.vm_opcode.vm.v[:2]) + 1):
            self.assertEqual(
                self.vm_opcode.vm.v[i],
                self.vm_opcode.vm.mem.fetch_byte(0x100 + i)
            )
