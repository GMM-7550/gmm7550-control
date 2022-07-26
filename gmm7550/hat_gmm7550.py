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
