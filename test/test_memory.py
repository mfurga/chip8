#
# CHIP-8 interpreter.
#
# Copyright (C) 2018 Mateusz Furga
# This software is released under the MIT license.

import unittest
from chip8.memory import Memory


class TestVMMemory(unittest.TestCase):

    def setUp(self):
        self.mem = Memory()

    def test_method_store_byte(self):
        # Checks off-by-one error
        with self.assertRaises(ValueError):
            self.mem.store_byte(0x1000, 0xff)

        # Checks negative address
        with self.assertRaises(ValueError):
            self.mem.store_byte(-0x100, 0xff)

        # Checks byte overflow
        self.assertTrue(self.mem.store_byte(0x0, 0xffff))

    def test_method_fetch_byte(self):
        # Checks off-by-one error
        with self.assertRaises(ValueError):
            byte = self.mem.fetch_byte(0x1000)

        # Checks negative address
        with self.assertRaises(ValueError):
            byte = self.mem.fetch_byte(-0x100)

        # Checks fetch byte
        self.mem.store_byte(0x0, 0xff)
        byte = self.mem.fetch_byte(0x0)
        self.assertEqual(byte, 0xff)

    def test_method_store_word(self):
        # Check buffer overflow error
        with self.assertRaises(ValueError):
            self.mem.store_word(0xfff, 0xeeff)

        # Checks negative address
        with self.assertRaises(ValueError):
            self.mem.store_word(-0x100, 0xffff)

        # Checks word overflow
        self.assertTrue(self.mem.store_word(0x0, 0xffffff))

        # Checks store word
        self.mem.store_word(0x0, 0xaabb)
        self.assertEqual(self.mem.fetch_byte(0x0), 0xaa)
        self.assertEqual(self.mem.fetch_byte(0x1), 0xbb)

    def test_method_fetch_word(self):
        # Checks too high address
        with self.assertRaises(ValueError):
            word = self.mem.fetch_word(0x1000)

        # Checks negative address
        with self.assertRaises(ValueError):
            word = self.mem.fetch_word(-0x100)

        # Checks fetch word
        self.mem.store_word(0x0, 0xffee)
        self.mem.store_byte(0x2, 0xdd)
        self.assertEqual(self.mem.fetch_word(0x0), 0xffee)
        self.assertEqual(self.mem.fetch_word(0x1), 0xeedd)
        self.assertEqual(self.mem.fetch_word(0x2), 0xdd00)

    def test_method_store_many(self):
        # Checks buffer overflow error
        with self.assertRaises(ValueError):
            self.mem.store_many(0x1000 - 3, [0xff, 0xff, 0xff, 0xff])

        # Checks negative address
        with self.assertRaises(ValueError):
            self.mem.store_many(-0x100, 'ABC')

        # Checks byte overflow
        self.assertTrue(self.mem.store_many(0x1000 - 2, [0xffff, 0xeee]))

        # Checks store many
        self.assertTrue(self.mem.store_many(0x1000 - 4, [0xaa, 0xbb, 0xcc, 0xdd]))
        self.assertEqual(self.mem.fetch_word(0x1000 - 4), 0xaabb)
        self.assertEqual(self.mem.fetch_word(0x1000 - 2), 0xccdd)

    def test_method_fetch_many(self):
        # Checks too high address
        with self.assertRaises(ValueError):
            data = self.mem.fetch_many(0x1000, 1)

        # Checks too high lenght
        with self.assertRaises(ValueError):
            data = self.mem.fetch_many(0x0, 0x1001)

        # Checks negative address
        with self.assertRaises(ValueError):
            data = self.mem.fetch_many(-0x100, 10)

        # Checks fetch many
        self.mem.store_many(0x0, [0xaa, 0xbb, 0xcc])

        self.assertEqual(self.mem.fetch_many(0x0, 3), bytearray([0xaa, 0xbb, 0xcc]))
        self.assertEqual(self.mem.fetch_many(0x2, 3), bytearray([0xcc, 0x00, 0x00]))
        self.assertEqual(self.mem.fetch_many(0xffe, 2), bytearray([0x00, 0x00]))
