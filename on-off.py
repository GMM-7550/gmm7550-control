#!/usr/bin/env python

import gpio
import time

PWR_ON = 494
MR = 492
DCDC_OFF = 470

def setup_gpio():
    gpio.setup(PWR_ON,   gpio.OUT, initial = False)
    gpio.setup(MR,       gpio.OUT, initial = True)
    gpio.setup(DCDC_OFF, gpio.OUT, initial = True)

    return None

def test():
    io = setup_gpio()

    gpio.set(PWR_ON, gpio.LOW)
    gpio.set(MR, gpio.HIGH)
    gpio.set(DCDC_OFF, gpio.HIGH)

    time.sleep(1)

    print("Power ON")
    gpio.set(PWR_ON, gpio.HIGH)
    time.sleep(0.5)
    gpio.set(DCDC_OFF, gpio.LOW)
    time.sleep(0.5)
    gpio.set(MR, gpio.LOW)

    time.sleep(10)

    print("Power Off")
    gpio.set(MR, gpio.HIGH)
    time.sleep(1)
    gpio.set(DCDC_OFF, gpio.HIGH)
    gpio.set(PWR_ON, gpio.LOW)

    gpio.cleanup()

if __name__ == '__main__':
    test()
