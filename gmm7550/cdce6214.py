
from time import sleep
from gmm7550.sem_smbus import i2c_msg

class CDCE6214:

    EEPROM_SIZE = 64 # 16-bit words
    EEPROM_F_PAGE_SIZE = 16
    EEPROM_PAGE_SIZE = 24

    def __init__(self, bus, addr=0x68):
        self.bus = bus
        self.addr = addr

    def read_reg(self, reg):
        ma = i2c_msg.write(self.addr, [(reg >> 8) & 0xff, reg & 0xff])
        md = i2c_msg.read(self.addr, 2)
        self.bus.acquire()
        self.bus.i2c_rdwr(ma, md)
        self.bus.release()
        d = list(md)
        return ((d[0]<<8) | d[1])

    def write_reg(self, reg, data):
        m = i2c_msg.write(self.addr, [ (reg >> 8) & 0xff,  reg & 0xff,
                                      (data >> 8) & 0xff, data & 0xff ])
        self.bus.acquire()
        self.bus.i2c_rdwr(m)
        self.bus.release()

    def read_eeprom(self):
        eeprom = []
        self.bus.acquire()
        self.write_reg(0x000b, 0x0000) # set start read address
        for i in range(self.EEPROM_SIZE):
            eeprom.append(self.read_reg(0x000c))
        self.bus.release()
        return eeprom

    def write_eeprom(self, eeprom):
        assert(len(eeprom) == self.EEPROM_SIZE,
               'EEPROM image size should be %d 16-bit words' % self.EEPROM_SIZE)
        self.bus.acquire()
        self.write_reg(0x000f, 0x5020) # unlock EEPROM
        self.write_reg(0x000d, 0x0000) # set start write address
        for w in eeprom:
            self.write_reg(0x000e, w)
            sleep(0.1)
        # TODO -- update CRC ???
        self.write_reg(0x000f, 0xA020) # lock EEPROM
        self.bus.release()

    def write_eeprom_page(self, page, eeprom_page):
        assert(page == 0 or page == 1,
               'EEPROM Page number should be 0 or 1 (got %d)' % page)
        assert(len(eeprom_page) == self.EEPROM_PAGE_SIZE,
               'EEPROM image size should be %d 16-bit words' % self.EEPROM_PAGE_SIZE)
        start_addr = self.EEPROM_F_PAGE_SIZE + page * self.EEPROM_PAGE_SIZE
        print('EEPROM start addr: %04x' % start_addr)
        self.bus.acquire()
        self.write_reg(0x000f, 0x5020) # unlock EEPROM
        self.write_reg(0x000d, start_addr) # set start write address
        for w in eeprom_page:
            print('%04x' % w)
            self.write_reg(0x000e, w)
            sleep(0.01) # 10ms > 8ms EEPROM word write time
        # TODO -- update CRC ???
        self.write_reg(0x000f, 0xA020) # lock EEPROM
        self.bus.release()

    def read_eeprom_string(self):
        eeprom = self.read_eeprom()
        s = '['
        for w in eeprom:
            s += '0x%04x,\n  ' % w
        s += ']'
        return s
