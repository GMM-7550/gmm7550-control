import spidev
from functools import reduce

class SPI():
    def __init__(self, bus, dev):
        self.spidev = spidev.SpiDev(bus, dev)
        self.spidev.max_speed_hz = 100000
        self.spidev.mode = 0

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
