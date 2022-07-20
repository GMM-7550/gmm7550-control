class GPIOpin:
    def __init__(self, pin):
        import gpio
        self.pin = pin

    def set_high(self):
        pass

    def set_low(self):
        pass

class sim_GPIOpin:
    def __init__(self, pin):
        self.pin = pin
        print("Init GPIO pin \"%s\"" % self.pin)

    def set_high(self):
        print("Set pin \"%s\" HIGH" % self.pin)

    def set_low(self):
        print("Set pin \"%s\" LOW" % self.pin)
