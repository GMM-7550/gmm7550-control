import spidev

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
