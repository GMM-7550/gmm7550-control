# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <ak@gmm7550.dev>

from setuptools import setup

setup(
    name = "gmm7550",
    version = "0.1.0",
    author = "Anton Kuzmin",
    author_email = "ak@gmm7550.dev",
    description = ("A set of tools to control GMM-7550 GateMage FPGA Module "
                   "from VisionFive or Raspberry-Pi boards"),
    license = "MIT",
    url = "https://github.com/gmm-7550/gmm7550-control",
    packages=['gmm7550'],
    scripts=['bin/gmm7550', 'bin/test-adm1177']
)
