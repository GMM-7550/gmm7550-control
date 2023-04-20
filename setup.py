# This file is a part of the GMM-7550 Control library
# <https://github.com/ak-fau/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

from setuptools import setup

setup(
    name = "gmm7550",
    version = "0.1.0",
    author = "Anton Kuzmin",
    author_email = "anton.kuzmin@cs.fau.de",
    description = ("A set of tools to control GMM-7550 GateMage FPGA Module "
                   "from VisionFive or Raspberry-Pi boards"),
    license = "MIT",
    url = "https://github.com/ak-fau/gmm7550-control",
    packages=['gmm7550'],
    scripts=['bin/gmm7550', 'bin/test-adm1177']
)
