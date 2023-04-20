# This file is a part of the GMM-7550 Control library
# <https://github.com/ak-fau/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

gpio = None

class GPIOpin:
    def __init__(self, pin):
        import gpio as _gpio
        global gpio; gpio = _gpio
        self.pin = pin
        self.state = gpio.LOW
        gpio.setup(self.pin, gpio.OUT)

    def _set(self):
        gpio.set(self.pin, self.state)

    def set_high(self):
        self.state = gpio.HIGH
        self._set()

    def set_low(self):
        self.state = gpio.LOW
        self._set()

    def get(self):
        return self.state

class sim_GPIOpin:
    def __init__(self, pin):
        self.pin = pin
        self.state = gpio.LOW
        print("Init GPIO pin \"%s\"" % self.pin)

    def set_high(self):
        self.state = gpio.HIGH
        print("Set pin \"%s\" HIGH" % self.pin)

    def set_low(self):
        self.state = gpio.LOW
        print("Set pin \"%s\" LOW" % self.pin)

    def get(self):
        print("Get pin \"%s\": %s" % (self.pin, self.state))
        return self.state
