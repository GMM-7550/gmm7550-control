# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <ak@gmm7550.dev>

class GPIO():

    OFF_SW_RST_N, OFF_POR_EN, OFF_CFG_FAILED_N, OFF_CFG_DONE = range(4)

    def __init__(self, bus, addr=0x74):
        self.bus = bus
        self.addr = addr

        self.bus.acquire()

        self.p0 = self.bus.read_byte_data(self.addr, 0)

        self.sw_rst = ((self.p0 >> self.OFF_SW_RST_N ) & 0x01) == 0
        self.por_en = ((self.p0 >> self.OFF_POR_EN   ) & 0x01) == 1

        self.p1 = self.bus.read_byte_data(self.addr, 1)

        self.cfg_mode = self.p1 & 0x0f
        self.spisel = (self.p1 >> 4) & 0x0f

        self.bus.write_byte_data(self.addr, 2, self.p0)
        self.bus.write_byte_data(self.addr, 3, self.p1)

        self.bus.write_byte_data(self.addr, 6,
            0xff & ~((1 << self.OFF_SW_RST_N) | (1 << self.OFF_POR_EN))
        )

        self.bus.write_byte_data(self.addr, 7, 0x00)

        self.bus.release()

    def _set_bit(self, bit_offset, value):
        if value:
            self.p0 |= (1 << bit_offset)
        else:
            self.p0 &= ~(1 << bit_offset)

        self.bus.acquire()
        self.bus.write_byte_data(self.addr, 2, self.p0)
        self.bus.release()

    def get_reset(self): return self.sw_rst
    def reset_on(self):
        self.sw_rst = True
        self._set_bit(self.OFF_SW_RST_N, 0)
    def reset_off(self):
        self.sw_rst = False
        self._set_bit(self.OFF_SW_RST_N, 1)

    def por_en(self): return self.por_en
    def cfg_mode(self): return self.cfg_mode
    def spisel(self): return self.spisel

    def _get_bit(self, bit_offset):
        self.bus.acquire()
        self.p0 = self.bus.read_byte_data(self.addr, 0)
        self.bus.release()
        return (self.p0 >> bit_offset) & 1

    def cfg_failed_n(self):
        return self._get_bit(self.OFF_CFG_FAILED_N)

    def cfg_done(self):
        return self._get_bit(self.OFF_CFG_DONE)
