# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

import sys
import string
import importlib

class Config:

    def __init__(self, cfg_name):
        super().__setattr__('name', cfg_name.lower())
        try:
            super().__setattr__('cfg', importlib.import_module('.%s' % self.name, package='gmm7550.configs'))
        except ImportError as e:
            print('Cannot load configuration: "%s"' % self.name, file=sys.stderr)
            print(e, file=sys.stderr)
            exit(1)

    def __getattr__(self, key):
        if hasattr(self.cfg, key):
            return getattr(self.cfg, key)
        else:
            return None

    def __setattr__(self, key, value):
        self.cfg.__setattr__(key, value)

    def name_or_value(self, d, k):
        if d:
            return d[k]
        else:
            return k
