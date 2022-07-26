class CDCE6214:

    def __init__(self, bus, addr=0x68):
        self.bus = bus
        self.addr = addr

    def read_reg(self, reg):
        return self.bus.read_word_data(self.addr, reg)

    def write_reg(self, reg, data):
        self.bus.write_word_data(self.addr, reg, data)

