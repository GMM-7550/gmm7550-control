
import time

from gmm7550 import gatemate as gm

class GMM7550():

    def __init__(self, cfg):
        self.cfg = cfg

        if self.cfg.gpio:
            from gmm7550.gpio import GPIOpin
        else:
            print('import GPIO')
            from gmm7550.gpio import sim_GPIOpin as GPIOpin

        self.power_en = GPIOpin(self.cfg.name_or_value(self.cfg.gpio, 'power_en'))
        self.power_en.set_low()
        self.dcdc_dis = GPIOpin(self.cfg.name_or_value(self.cfg.gpio, 'dcdc_dis'))
        self.dcdc_dis.set_high()
        self.mr = GPIOpin(self.cfg.name_or_value(self.cfg.gpio, 'mr'))
        self.mr.set_high()

        if self.cfg.i2c:
            from gmm7550.sem_smbus import SMBus
            self.i2c = SMBus(self.cfg.i2c)

        if self.cfg.id_i2c:
            from gmm7550.sem_smbus import SMBus
            self.id_i2c = SMBus(self.cfg.id_i2c)

    def start(self):
        self.power_en.set_high()
        self.dcdc_dis.set_low()
        time.sleep(0.2)
        self.mr.set_low()
