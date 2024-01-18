# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

board_name = "Raspberry-Pi"

gpio = {
    'power_en' : 4,
    'dcdc_dis' : 27,
    'mr' : 17
    }

i2c = 1

spi_bus = 0
spi_dev = 0
