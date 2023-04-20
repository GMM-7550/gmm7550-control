# This file is a part of the GMM-7550 Control library
# <https://github.com/ak-fau/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

import spidev
from functools import reduce

class SPI_NOR():
    PAGE_SIZE    = 256     # Programming page size
    SECTOR_SIZE  =  4*1024 # Smallest erase unit
    BLOCK32_SIZE = 32*1024
    BLOCK64_SIZE = 64*1024

class SPI():

    def __init__(self, bus, dev):
        self.spidev = spidev.SpiDev(bus, dev)
        self.spidev.max_speed_hz = 20000000
        self.spidev.mode = 0
        self.nor = SPI_NOR()

    def print_info(self):
        print('SPI Device Info:')
        id = self.spidev.xfer([0x9f, 0, 0, 0])
        print('JEDEC ID')
        print('  manufacturer: %02x' % id[1])
        print('   memory type: %02x' % id[2])
        print('      capacity: %02x' % id[3])
        uid_xfer = [0 for i in range(3 + 16)]
        uid_xfer.insert(0, 0x4b)
        uid = self.spidev.xfer(uid_xfer)
        uid = reduce(lambda s, b : s + " %02x" % b,
                     uid[4:],
                     'UID:')
        print(uid)

    def reset(self):
        self.spidev.xfer([0x66]) # RSTEN
        self.spidev.xfer([0x99]) # RST

    def read_status(self):
        data = self.spidev.xfer([0x05, 0x00])
        return data[1]

    def wait_idle(self):
        while True:
            sr = self.read_status()
            if (sr & 0x01) == 0x00:
                return

    def write_enable(self):
        self.spidev.xfer([0x06])
        sr = self.read_status()
        if (sr & 0x02) == 0x00:
            print('ERROR: Cannot enable SPI Write')
            return False
        return True

    def write_disable(self):
        self.spidev.xfer([0x04])

    def chip_erase(self):
        if self.write_enable():
            self.spidev.xfer([0x60])
            self.wait_idle()
            self.write_disable()

    def sector_erase(self, addr):
        xfer = [ 0x20, # SER
                 (addr >> 16) & 0xff,
                 (addr >>  8) & 0xff,
                  addr        & 0xff]
        if self.write_enable():
            self.spidev.xfer(xfer)
            self.wait_idle()
            self.write_disable()

    def write_page(self, addr, data):
        data.insert(0, addr & 0xff)
        addr >>= 8
        data.insert(0, addr & 0xff)
        addr >>= 8
        data.insert(0, addr & 0xff)
        data.insert(0, 0x02) # Page Program command

        self.wait_idle()
        if self.write_enable():
            self.spidev.xfer(data)
            self.wait_idle()
            self.write_disable()

    def read(self, addr, count = SPI_NOR.PAGE_SIZE):
        if count >= self.nor.PAGE_SIZE:
            count = self.nor.PAGE_SIZE
        xfer = [0x00 for i in range(count)]
        xfer.insert(0, addr & 0xff)
        addr >>= 8
        xfer.insert(0, addr & 0xff)
        addr >>= 8
        xfer.insert(0, addr & 0xff)
        xfer.insert(0, 0x03) # NORD -- Normal Read
        return self.spidev.xfer(xfer)[4:]

    def cfg(self, data):
        self.spidev.xfer3(list(data))
