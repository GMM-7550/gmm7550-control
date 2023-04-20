# This file is a part of the GMM-7550 Control library
# <https://github.com/ak-fau/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

import smbus2 as smbus
import threading

class SMBus(smbus.SMBus):

    def __init__(self, b):
        super().__init__(b)
        self.sem = threading.RLock()

    def acquire(self):
        return self.sem.acquire()

    def release(self):
        return self.sem.release()

class i2c_msg(smbus.i2c_msg):
    pass
