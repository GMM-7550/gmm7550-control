
gpio = None

class GPIOpin:
    def __init__(self, pin):
        import gpio as _gpio
        global gpio; gpio = _gpio
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)

    def set_high(self):
        gpio.set(self.pin, gpio.HIGH)

    def set_low(self):
        gpio.set(self.pin, gpio.LOW)

class sim_GPIOpin:
    def __init__(self, pin):
        self.pin = pin
        print("Init GPIO pin \"%s\"" % self.pin)

    def set_high(self):
        print("Set pin \"%s\" HIGH" % self.pin)

    def set_low(self):
        print("Set pin \"%s\" LOW" % self.pin)
