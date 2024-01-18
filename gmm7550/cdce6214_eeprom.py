# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <ak@gmm7550.dev>

factory = False

eeprom = [
  ######### Default (factory) page
  0x7002, 0x487f, 0x1b12, 0x0000, 0x28a0, 0x4cd0, 0x0700, 0x6280,
  0x8340, 0x5a2d, 0x2428, 0x142d, 0x166e, 0x250a, 0x0434, 0x0102,
########### Page 0
  0xa801, 0x00ec, 0x4000, 0x2470, 0x0200, 0x0060, 0x0000, 0x0000,
  0x0000, 0x0a22, 0x1800, 0x00d8, 0x8000, 0x0c40, 0x0000, 0x0c48,
  0x0000, 0x0d08, 0x0000, 0x1008, 0x0000, 0x0000, 0x0000, 0x1000,
########### Page 1
  0xa440, 0x00ec, 0x4000, 0x2470, 0x0200, 0x0060, 0x0000, 0x0000,
  0x0000, 0x0a22, 0x1800, 0x00d8, 0x0000, 0x0c50, 0x0000, 0x0c50,
  0x0000, 0x0d10, 0x0000, 0x1100, 0x0000, 0x0000, 0x0000, 0x0000
]

if factory :
    # Factory page 0
    page0_gmm = [
        0xa801, 0x00ec, 0x4000, 0x2470, 0x0200, 0x0060, 0x0000, 0x0000,
        0x0000, 0x0a22, 0x1800, 0x00d8, 0x8000, 0x0c40, 0x0000, 0x0c48,
        0x0000, 0x0d08, 0x0000, 0x1008, 0x0000, 0x0000, 0x0000, 0x1000,
    ]
else:
    page0_gmm = [
        0x2020, 0x0446, 0x4000, 0x1c60, 0x0200, 0x0060, 0x0000, 0x0000,
        0x0000, 0x0a22, 0x1800, 0x00d8, 0x0000, 0x0c10, 0x0200, 0x0c00,
        0x0000, 0xc000, 0x0003, 0x0080, 0x0020, 0x0000, 0x0000, 0x1000
    ]
