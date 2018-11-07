#
# CHIP-8 interpreter.
#
# Copyright (C) 2018 Mateusz Furga
# This software is released under the MIT license.

import pygame

FONTS = (
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80   # F
)

# https://www.pygame.org/docs/ref/key.html
KEY_MAP = {
    0x0: pygame.K_KP0, 0x1: pygame.K_KP1,
    0x2: pygame.K_KP2, 0x3: pygame.K_KP3,
    0x4: pygame.K_KP4, 0x5: pygame.K_KP5,
    0x6: pygame.K_KP6, 0x7: pygame.K_KP7,
    0x8: pygame.K_KP8, 0x9: pygame.K_KP9,
    0xA: pygame.K_a,   0xB: pygame.K_b,
    0xC: pygame.K_c,   0xD: pygame.K_d,
    0xE: pygame.K_e,   0xF: pygame.K_f
}

HEIGHT = 32
WIDTH  = 64
COLORS = (
    pygame.Color(0, 0, 0, 255),       # Black
    pygame.Color(255, 255, 255, 255)  # White
)


class Display(object):
    """
    CHIP-8 display class.

    Source:
        http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#dispcoords

    The original implementation of the Chip-8 language
    used a 64x32-pixel monochrome display with this format:
                +-----------------------+
                |(0, 0)          (63, 0)|
                |                       |
                |                       |
                |(0, 31)        (63, 31)|
                +-----------------------+
    """

    def __init__(self, vm, width=WIDTH, height=HEIGHT, scale=1):
        self.vm = vm
        self.width = width
        self.height = height
        self.scale = scale

        self.init_display()

    def init_display(self):
        """
        Initializes the screen. Sets the width & the height of the screen
        multiplied by the scale.
        """
        pygame.display.init()
        pygame.display.set_caption('CHIP-8 Emulator')
        self.surface = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale),
            0, 8
        )

    def load_fonts(self):
        """Loads font data into memory in the range of 0x0 to 0x49."""
        self.vm.mem.store_many(0, FONTS)

    def load_sound(self, fname):
        """Loads sound effects using the pygame API."""
        pygame.mixer.init()
        pygame.mixer.music.load(fname)

    def set_pixel(self, point, color):
        """Sets the pixel to on or off at the given point (X, Y)."""
        pygame.draw.rect(
            self.surface, COLORS[color],
            (point[0] * self.scale, point[1] * self.scale,
                self.scale, self.scale)
        )

    def get_pixel(self, point):
        """Gets the value of the pixel at the given point (X, Y)."""
        color = self.surface.get_at(
            (point[0] * self.scale, point[1] * self.scale)
        )
        color = 1 if color == COLORS[1] else 0
        return color

    def draw_sprite(self, point, data):
        """Displays the bytes of data as sprites on the screen at coordinates (X, Y)."""
        self.vm.v[0xf] = 0

        for iy, y in enumerate(data):
            coord_y = (point[1] + iy) % self.height

            for ix, x in enumerate('{:08b}'.format(y)):
                coord_x = (point[0] + ix) % self.width
                color = int(x)
                current_color = self.get_pixel((coord_x, coord_y))
                if color == 1 and current_color == 1:
                    self.vm.v[0xf] |= 1
                self.set_pixel((coord_x, coord_y), color ^ current_color)

        pygame.display.flip()

    def clear_display(self):
        """Fills all the pixels on the screen in the same color (default black)."""
        self.surface.fill(COLORS[0])
        pygame.display.flip()
