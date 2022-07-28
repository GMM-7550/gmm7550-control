
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
