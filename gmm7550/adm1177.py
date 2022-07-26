class ADM1177:
    def __init__(self, bus, adr=0, r_sense=0.050):
        self.bus = bus
        self.addr = 0x58 | (adr & 0x03)
        self.cmd_mask = 0
        self.set_range(0)
        self.i_range = 105.84 # mV
        self.r_sense = r_sense

    def set_range(self, r):
        if r == 0:
            self.cmd_mask &= ~0x40
            self.v_range = 26.35 # 14:1 * 1.902V
        else:
            self.cmd_mask |= 0x40
            self.v_range = 6.65 # 7:2 * 1.902V

        self.bus.write_byte(self.addr, self.cmd_mask)
 
    def start_vi_cont(self):
        self.bus.write_byte(self.addr, self.cmd_mask | 0x05)

    def stop_vi(self):
        self.bus.write_byte(self.addr, self.cmd_mask)

    def get_vi(self):
        # read three bytes
        v_raw = b[0] << 4 | ((b[2] >> 4) & 0x0f)
        i_raw = b[1] << 4 | (b[2] & 0x0f)
        v = v_raw * (self.v_range / 4096)
        i = i_raw * (self.i_range / 4096) / self.r_sense
        return (v, i) # (V, mA)

