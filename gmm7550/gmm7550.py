
import time

from gmm7550 import gatemate as gm
from gmm7550 import hat_gmm7550

class GMM7550():

    def __init__(self, cfg):
        self.cfg = cfg

        self.hat = hat_gmm7550.HAT_GMM7550(cfg)

    def start(self):
        self.hat.power_en.set_high()
        self.hat.dcdc_dis.set_low()
        time.sleep(0.2)
        self.hat.mr.set_low()
