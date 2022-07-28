from gmm7550.sem_smbus import i2c_msg

V_CONT = 0x01
V_ONCE = 0x02
I_CONT = 0x04
I_ONCE = 0x08
VRANGE = 0x10
STATUS_RD = 0x40
EXT_CMD_R = 0x80

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
            self.cmd_mask &= ~VRANGE
            self.v_range = 26.35 # 14:1 * 1.902V
        else:
            self.cmd_mask |= VRANGE
            self.v_range = 6.65 # 7:2 * 1.902V

        self.bus.acquire()
        self.bus.write_byte(self.addr, self.cmd_mask)
        self.bus.release()
 
    def start_vi_cont(self):
        self.bus.acquire()
        self.bus.write_byte(self.addr, self.cmd_mask | V_CONT | I_CONT)
        self.bus.release()

    def stop_vi(self):
        self.bus.acquire()
        self.bus.write_byte(self.addr, self.cmd_mask)
        self.bus.release()

    def get_vi(self):
        m = i2c_msg.read(self.addr, 3)
        self.bus.acquire()
        self.bus.i2c_rdwr(m)
        self.bus.release()
        b = list(m)
        v_raw = b[0] << 4 | ((b[2] >> 4) & 0x0f)
        i_raw = b[1] << 4 | (b[2] & 0x0f)
        v = v_raw * (self.v_range / 4096)
        i = i_raw * (self.i_range / 4096) / self.r_sense
        return (v, i) # (V, mA)

    def get_vi_string(self):
        return "V = %4.2f V,  I = %5.0f mA" % self.get_vi()

