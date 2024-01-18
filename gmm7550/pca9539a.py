# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <ak@gmm7550.dev>

class PCA9539A:

    def __init__(self, bus, a=0):
        self.bus = bus
        self.addr = 0x74 | (a & 0x03)

    def get_input(self):
        return self.bus.read_word_data(self.addr, 0)

    def get_output(self):
        return self.bus.read_word_data(self.addr, 2)

    def get_inversion(self):
        return self.bus.read_word_data(self.addr, 4)

    def get_config(self):
        return self.bus.read_word_data(self.addr, 6)

    def set_output(self, data):
        self.bus.write_word_data(self.addr, 2, data)

    def set_inversion(self, data):
        self.bus.write_word_data(self.addr, 4, data)

    def set_config(self, data):
        self.bus.write_word_data(self.addr, 6, data)
