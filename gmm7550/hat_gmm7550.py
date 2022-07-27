from gmm7550.adm1177 import ADM1177

class HAT_GMM7550():

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

        if self.cfg.i2c is not None:
            import gmm7550.sem_smbus as smbus
            self.i2c = smbus.SMBus(self.cfg.i2c)
            self.adm1177 = ADM1177(self.i2c)
            self.adm1177.set_range(1)
            self.adm1177.start_vi_cont()
            print("V = %4.2f V,  I = %5.0f mA" % self.adm1177.get_vi())
        else:
            self.i2c = None
