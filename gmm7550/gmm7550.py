
from time import sleep

from gmm7550 import gatemate as gm
from gmm7550 import hat_gmm7550

from gmm7550.pca9539a import PCA9539A
from gmm7550.cdce6214 import CDCE6214

class I2C_GPIO:
    srst       = 0x0001
    por_en     = 0x0002
    cfg_failed = 0x0004
    cfg_done   = 0x0008
    refsel     = 0x0010
    hwswctrl   = 0x0020
    gpio1      = 0x0040
    gpio4      = 0x0080

# Input signals
I2C_GPIO_config    = (I2C_GPIO.cfg_failed | I2C_GPIO.cfg_done |
                      I2C_GPIO.gpio1 | I2C_GPIO.gpio4)

# Active LOW input signals
I2C_GPIO_inversion = I2C_GPIO.cfg_failed

class GMM7550():

    def __init__(self, cfg):
        self.cfg = cfg
        self.hat = hat_gmm7550.HAT_GMM7550(cfg)
        self.i2c = self.hat.i2c # local copy

        self.pwr_rampup = 0.1
        self.mr_delay = 0.1 # TPS3840 CT = 0.1uF --> ~60ms < 100ms == 0.1 s

        self.active = False
        # these devices are not powered-up yet
        self.i2c_gpio = None
        self.pll = None

        # Hardware defaults
        self.refsel = 0
        self.hwswctrl = 1
        # self.cfg_mode = gm.CFG_mode.SPI_ACTIVE_0
        self.cfg_mode = gm.CFG_mode.JTAG
        self.spi_sel = [0, 0, 0, 0]
        self.soft_reset = True

    def is_active(self):
        return self.active

    def _restore_i2c_gpio_state(self):
        self.i2c.acquire()
        self.i2c_gpio.set_inversion(I2C_GPIO_inversion)
        out = 0x0000
        for i in range(3):
            out |= self.spi_sel[i] << (12+i)
        out |= self.cfg_mode.value << 8
        out |= I2C_GPIO.gpio1 | I2C_GPIO.gpio4
        if self.refsel:
            out |= I2C_GPIO.refsel
        if self.hwswctrl:
            out |= I2C_GPIO.hwswctrl
        out |= I2C_GPIO.por_en
        if not self.soft_reset:
            out |= I2C_GPIO.srst
        self.i2c_gpio.set_output(out)
        self.i2c_gpio.set_config(I2C_GPIO_config)
        self.i2c.release()

    def soft_reset_on(self):
        self.soft_reset = True
        if self.active:
            self.i2c.acquire()
            o = self.i2c_gpio.get_output()
            o &= ~I2C_GPIO.srst
            self.i2c_gpio.set_output(o)
            self.i2c.release()

    def soft_reset_off(self):
        self.soft_reset = False
        if self.active:
            self.i2c.acquire()
            o = self.i2c_gpio.get_output()
            o |= I2C_GPIO.srst
            self.i2c_gpio.set_output(o)
            self.i2c.release()

    def soft_reset_pulse(self):
        self.soft_reset_on()
        sleep(self.mr_delay)
        self.soft_reset_off()

    def start(self):
        self.hat.power_en.set_high()
        self.hat.dcdc_dis.set_low()
        sleep(self.pwr_rampup)
        self.hat.mr.set_low()
        sleep(self.mr_delay)
        self.active = True

        self.i2c_gpio = PCA9539A(self.i2c)
        self._restore_i2c_gpio_state()
        self.soft_reset_off()
        self.pll = CDCE6214(self.i2c)
        print(self.hat.adm1177.get_vi_string())

    def poweroff(self):
        self.active = False
        self.hat.mr.set_high()
        self.hat.dcdc_dis.set_high()
        self.hat.power_en.set_low()
