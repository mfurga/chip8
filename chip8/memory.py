'''
    CHIP-8 emulator.

    Copyright (C) 2018 Mateusz Furga
    This software is released under the MIT license.
'''


class Memory(object):
    '''
    CHIP-8 memory class.

    Source:
        http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#2.1

    The Chip-8 language is capable of accessing up to 4KB (4,096 bytes)
    of RAM, from location 0x000 (0) to 0xFFF (4095). The first 512 bytes,
    from 0x000 to 0x1FF, are where the original interpreter was located,
    and should not be used by programs.
    '''

    def __init__(self):
        '''
        Allocates 4KB (4096 bytes) for program memory.
        '''
        self._mem = bytearray(0x1000)

    def store_byte(self, addr, data):
        '''
        Stores 1 byte of data at the given address.
        '''
        if addr < 0 or addr >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        self._mem[addr] = data & 0xff
        return True

    def fetch_byte(self, addr):
        '''
        Fetches 1 byte of data from the given address.
        '''
        if addr < 0 or addr >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        return self._mem[addr]

    def store_word(self, addr, data):
        '''
        Stores word (2 bytes) of data at the given address.
        '''
        if addr < 0 or addr + 1 >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        self._mem[addr] = (data >> 8) & 0xff
        self._mem[addr + 1] = data & 0xff
        return True

    def fetch_word(self, addr):
        '''
        Fetches word (2 bytes) of data from the given address.
        '''
        if addr < 0 or addr + 1 >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        return (self._mem[addr] << 8 | self._mem[addr + 1])

    def store_many(self, addr, data):
        '''
        Stores many bytes of data at the given address.
        '''
        if addr < 0 or addr + len(data) - 1 >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        for i, byte in enumerate(data):
            self._mem[addr + i] = byte & 0xff
        return True

    def fetch_many(self, addr, lenght):
        '''
        Fetched many bytes of data from the given address.
        '''
        if addr < 0 or addr + lenght - 1 >= len(self._mem):
            raise ValueError  # TODO: Make custom exception
        return self._mem[addr:addr + lenght]
