# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

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
            print(self.adm1177.get_vi_string())
        else:
            self.i2c = None
