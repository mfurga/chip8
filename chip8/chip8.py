#!/usr/bin/env python2
#
# CHIP-8 interpreter.
#
# Copyright (C) 2018 Mateusz Furga
# This software is released under the MIT license.

import argparse
import pygame

from display import Display
from memory import Memory
from opcode import Opcode

# Settings
PROGRAM_COUNTER_START = 0x200
STACK_POINTER_START   = 0x50
SOUND_EFFECT_FILENAME = 'buzz.wav'


class Chip8(object):
    """
    CHIP-8 main class.

    Sources:
        https://en.wikipedia.org/wiki/CHIP-8
        http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

    CHIP-8 has:
    - 16 x 8-bit general purpose registers (V0 - VF) (0 through F)
    - 1 x 16-bit index register called I (store memory address)
    - 1 x 16-bit program counter (PC) (store currently executing address)
    - 1 x 8-bit stack pointer (SP) (point to the topmost level of stack)
    - 1 x 8-bit delay timer (DT)
    - 1 x 8-bit sound timer (ST)
    - 16 x 16 bit array using for stack
    """

    def __init__(self, data, scale=10):
        self.mem = Memory()
        self.mem.store_many(PROGRAM_COUNTER_START, data)

        self.opcode = Opcode(self)
        self.display = Display(self, scale=scale)
        self.display.load_fonts()
        self.display.load_sound(SOUND_EFFECT_FILENAME)

        self.v = bytearray(0x10)
        self.pc = PROGRAM_COUNTER_START
        self.sp = STACK_POINTER_START

        self.dt = 0
        self.st = 0
        self.i = 0

    @classmethod
    def load_program_from_file(cls, fname, scale):
        """Loads up program data into memory."""
        with open(fname, 'rb') as f:
            data = bytearray(f.read())
        return cls(data, scale)

    def run(self, delay):
        """Fetches the opcode (2 bytes) from the memory and executes it."""
        running = True
        while running:
            pygame.time.wait(delay)
            opcode = self.mem.fetch_word(self.pc)

            self.pc += 2
            self.opcode.instruction_lookup(opcode)
            self.opcode.decrement_registers()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.QUIT:
                    running = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        './chip8.py',
        description='CHIP-8 interpreter',
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=100, width=150))

    parser.add_argument('program', help='CHIP-8 ROM')

    parser.add_argument('-d', '--delay', type=int, default=1,
                        help='Specify delay for every instruction (default=1ms)')

    parser.add_argument('-s', '--scale', type=int, default=10,
                        help='Specify scale for width & height (default=10)')

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Enable verbose output')  # TODO: Import logging

    args = parser.parse_args()
    vm = Chip8.load_program_from_file(args.program, args.scale)
    vm.run(args.delay)
