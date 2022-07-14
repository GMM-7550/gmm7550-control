#!/bin/bash

(sleep 2 && firefox --no-remote -P gmm7550 --kiosk --new-window  http://localhost:5006/gmm7550_panel) &

#/usr/bin/panel serve --autoreload --show gmm7550_panel.py
/usr/bin/panel serve --autoreload gmm7550_panel.py
