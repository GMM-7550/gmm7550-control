import gpio

GPIO_PIN_NUM = {
    'mr': 492,
    'pwr_on': 494,
    'dcdc_off': 470,
}

def gpio_init():
    gpio.setup(GPIO_PIN_NUM['mr'],       gpio.OUT, initial = True)
    gpio.setup(GPIO_PIN_NUM['pwr_on'],   gpio.OUT, initial = False)
    gpio.setup(GPIO_PIN_NUM['dcdc_off'], gpio.OUT, initial = True)

def vin_on():
    gpio.set(GPIO_PIN_NUM['pwr_on'], gpio.HIGH)

def vin_off():
    gpio.set(GPIO_PIN_NUM['pwr_on'], gpio.LOW)

def dcdc_enable():
    gpio.set(GPIO_PIN_NUM['dcdc_off'], gpio.LOW)

def dcdc_disable():
    gpio.set(GPIO_PIN_NUM['dcdc_off'], gpio.HIGH)

def reset_on():
    gpio.set(GPIO_PIN_NUM['mr'], gpio.HIGH)

def reset_off():
    gpio.set(GPIO_PIN_NUM['mr'], gpio.LOW)

