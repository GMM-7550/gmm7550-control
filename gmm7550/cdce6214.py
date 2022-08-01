
from gmm7550.sem_smbus import i2c_msg

class CDCE6214:

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
        # self.bus.acquire()
        self.write_reg(0x000b, 0x0000) # set start read address
        for i in range(64):
            eeprom.append(self.read_reg(0x000c))
        # self.bus.release()
        return eeprom

    def write_eeprom(self, eeprom):
        assert(len(eeprom) == 64, "EEPROM image size should be 64 16-bit words")
        # self.bus.acquire()
        self.write_reg(0x000f, 0x5020) # unlock EEPROM
        self.write_reg(0x000d, 0x0000) # set start write address
        for w in eeprom:
            self.write_reg(0x000e, w)
        # TODO -- update CRC ???
        self.write_reg(0x000f, 0xA020) # lock EEPROM
        # self.bus.release()

    def read_eeprom_string(self):
        eeprom = self.read_eeprom()
        s = '['
        for w in eeprom:
            s += '0x%04x,\n  ' % w
        s += ']'
        return s

