#!/usr/bin/env python3

from time import sleep

import sem_smbus as smbus
import adm1177

b = smbus.SMBus(1)
a = adm1177.ADM1177(b)

a.set_range(1)
a.start_vi_cont()

for i in range(10):
    print("V = %4.2f V,  I = %5.0f mA" % a.get_vi())
    sleep(.5)
