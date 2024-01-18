# This file is a part of the GMM-7550 Control library
# <https://github.com/gmm-7550/gmm7550-control.git>
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2022-2023 Anton Kuzmin <anton.kuzmin@cs.fau.de>

import panel as pn
from time import sleep

import sem_smbus as smbus

import gmm7550 as gmm
import hat_gmm7550 as hat

i2c = smbus.SMBus(1)

gmm_io = None

# gmm_io = gmm.GPIO(i2c)

Vin_enable  = False
DCDC_enable = False
MasterReset = True
SoftReset   = False

hat.gpio_init()

#
# Input Power
#

Vin_status = pn.indicators.BooleanStatus(value=Vin_enable, color='success', align='center')
Vin_button = pn.widgets.Button(name='On', width=30, align='center')

def vin_action(e):
    global Vin_enable
    global DCDC_enable
    global i2c
    global gmm_io

    Vin_enable = not Vin_enable
    Vin_status.value = Vin_enable
    if Vin_enable:
       Vin_button.name = 'Off'
       hat.vin_on()
       if DCDC_enable and not MasterReset and not gmm_io:
           sleep(.2)
           gmm_io = gmm.GPIO(i2c)
    else:
       Vin_button.name = 'On'
       gmm_io = None
       hat.vin_off()

Vin_button.on_click(vin_action)

#
# DC-DC Enable
#
dcdc_status = pn.indicators.BooleanStatus(value=DCDC_enable, color='success', align='center')
dcdc_button = pn.widgets.Button(name='On', width=30, align='center')

def dcdc_action(e):
    global Vin_enable
    global DCDC_enable
    global i2c
    global gmm_io

    DCDC_enable = not DCDC_enable
    dcdc_status.value = DCDC_enable
    if DCDC_enable:
       dcdc_button.name = 'Off'
       hat.dcdc_enable()
       if Vin_enable and not MasterReset and not gmm_io:
           sleep(.2)
           gmm_io = gmm.GPIO(i2c)
    else:
       dcdc_button.name = 'On'
       gmm_io = None
       hat.dcdc_disable()

dcdc_button.on_click(dcdc_action)

#
# Master Reset
#
mr_status = pn.indicators.BooleanStatus(value=MasterReset, color='warning', align='center')
mr_button = pn.widgets.Button(name='Off', width=30, align='center')

def mr_action(e):
    global MasterReset
    global SoftReset
    global gmm_io
    MasterReset = not MasterReset
    mr_status.value = MasterReset or SoftReset
    if MasterReset:
       mr_button.name = 'Off'
       gmm_io = None
       hat.reset_on()
    else:
       mr_button.name = 'On'
       hat.reset_off()
       if Vin_enable and DCDC_enable and not gmm_io:
           sleep(.2)
           gmm_io = gmm.GPIO(i2c)
           SoftReset = gmm_io.get_reset()

mr_button.on_click(mr_action)

mr_pulse  = pn.widgets.Button(name='Pulse', width=30, align='center')

def mr_pulse_action(e):
    global MasterReset
    global i2c

    MasterReset = True
    mr_status.value = True
    hat.reset_on()
    sleep(0.5)
    hat.reset_off()
    if Vin_enable and DCDC_enable:
        sleep(.2)
        gmm_io = gmm.GPIO(i2c)
    MasterReset = False
    mr_status.value = False
    mr_button.name = 'On'

mr_pulse.on_click(mr_pulse_action)

#
# Software Reset
#

sw_rst_status = pn.indicators.BooleanStatus(value=SoftReset, color='warning', align='center')
sw_rst_button = pn.widgets.Button(name='Off', width=30, align='center')

def sw_rst_action(e):
    global MasterReset
    global SoftReset
    global gmm_io

    if not MasterReset and gmm_io:
        SoftReset = not SoftReset
        mr_status.value = MasterReset or SoftReset
        if SoftReset:
           sw_rst_button.name = 'Off'
           sw_rst_status.value = True
           gmm_io.reset_on()
        else:
           sw_rst_button.name = 'On'
           sw_rst_status.value = False
           gmm_io.reset_off()

sw_rst_button.on_click(sw_rst_action)

sw_rst_pulse  = pn.widgets.Button(name='Pulse', width=30, align='center')

def sw_rst_pulse_action(e):
    global MasterReset
    global SoftReset
    global gmm_io
    SoftReset = True
    mr_status.value = True
    sw_rst_status.value = True
    gmm_io.reset_on()
    sleep(0.5)
    gmm_io.reset_off()
    SoftReset = False
    mr_status.value = MasterReset or SoftReset
    sw_rst_status.value = SoftReset

sw_rst_pulse.on_click(sw_rst_pulse_action)


hat_column = pn.Column('## HAT Control', width=500)
label_width = 110
hat_column.append(pn.Row(pn.pane.Markdown('### Vin Power', width=label_width), Vin_status, Vin_button))
hat_column.append(pn.Row(pn.pane.Markdown('### DCDC Enable', width=label_width), dcdc_status, dcdc_button))
hat_column.append(pn.Row(pn.pane.Markdown('### Master Reset', width=label_width), mr_status, mr_button, mr_pulse))

gmm_column = pn.Column('## GMM Control', width=500)
label_width = 110
gmm_column.append(pn.Row(pn.pane.Markdown('### Soft Reset', width=label_width), sw_rst_status, sw_rst_button, sw_rst_pulse))

# hat_column.append(pn.Row(pn.pane.Markdown('### Config Status', width=label_width), cfg_status))

main_control_tab = pn.Row(hat_column, gmm_column,
                          name="GMM-7550 Control")

tabs = []

tabs.append(main_control_tab)

#gm_term = pn.widgets.Terminal(
#    name="GMM-7550 Console",
#    options={"cursorBlink":True},
#    width=800)

#gm_term.subprocess.run("picocom", "-q", "-b 115200", "/dev/ttyUSB0")
#gm_term.subprocess.run("bash")

#terminal_tab = pn.Row(gm_term, name="GMM-7550 Terminal")
#tabs.append(terminal_tab)

tabs.append(pn.pane.Markdown("""
# Configuration settings

## VisionFive IO interfaces

- GPIO
    - power enable (pin*N*)
    - DC-DC enable (pin*N*)
    - Master Reset (pin*N*)
- ID EEPROM I<sup>2</sup>C bus (`/dev/i2c`*x*)
- GMM-7550 I<sup>2</sup>C bus (`/dev/i2c`*x*)
    - ADM1177 address and parameters (?)
    - PLL address and parameters
    - IO expander pins/configuration
- SPI bus (`/dev/spidev`*x*.*y*)
    - Fmax
    - mode (0/3)
- UART (`/dev/ttyS*x*`)
    - baudrate

## Whatever else...
""",
                             name="Settings"))

tabs.append(pn.pane.Markdown("# SPI", name="SPI"))
tabs.append(pn.pane.Markdown("# PLL", name="PLL"))
tabs.append(pn.pane.Markdown("# ID EEPROM", name="ID EEPROM"))

tabs.append(pn.pane.Markdown("""
# Reference materials

- [project repository at GitHub](https://github.com/gmm-7550/gmm7550/)

## GateMate FPGA

- configuration modes

## HAT

- Schematic
- PCB assembly drawing
- VisionFive GPIO assignment
- ADM1177 datasheet
- ID EEPROM (I2C1)
- RPi HAT ID EEPROM format

## GMM-7550

- Schematic
- PCB assembly drawing
- SPI switch configuration
- I2C IO control
- PCAxxxx
- CDCE...
- SPI-NOR M25...
""",
                         name="Documentation"))

tabs.append(pn.pane.Markdown("""
# Raw hardware access

## HAT

- ADM1177 (I2C0)
- GPIO
- ID EEPROM (I2C1)

## GMM-7550

- I2C GPIO
- PLL
- SPI
- UART
""",
                             name="Debug"))

top_tabs = pn.Tabs(*tabs,
                   dynamic=True,
                   sizing_mode="stretch_width"
                   )

top_tabs.servable()
