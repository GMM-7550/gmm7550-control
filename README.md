# Control Utilities for GMM-7550 Module on RPi HAT

CLI and Web-based (Python panel) tools for VisionFive and Raspberry-Pi
single-board computers to control GateMate FPGA module (GMM-7550) on
the 40-pin GPIO adapter board.

## Command Line Options

```
[root@alarmpi ~]# gmm7550 --help
usage: gmm7550 [-h] [-V] [-v] [-b {visionfive,rpi,sim}] [-p {0,1}] [-s {0..15}] [-m {spi_active,spi_passive,jtag}] [-S {0,1,2,3}]
               {power,on,off,reset,pll,spi,id} ...

Command line tool to program, test, and control GMM-7550 module connected via HAT adapter board to a VisionFive or Raspberry Pi SBC

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose         be more verbose
  -b {visionfive,rpi,sim}, --board {visionfive,rpi,sim}
                        select target hardware configuration
  -p {0,1}, --pll-page {0,1}
                        PLL configuration EEPROM page
  -s {0..15}, --spi-sel {0..15}
                        select SPI multiplexer configuration
  -m {spi_active,spi_passive,jtag}, --mode {spi_active,spi_passive,jtag}
                        set FPGA configuration mode
  -S {0,1,2,3}, --spi-mode {0,1,2,3}
                        SPI mode for SPI configuration

Commands:
  {power,on,off,reset,pll,spi,id}
```

## PLL Configuration

The PLL chip configuration registers and EEPROM may be accessed with
a `pll` sub-command.

```
# gmm7550 pll --help
usage: gmm7550 pll [-h] [-e] [-P {0,1}]

options:
  -h, --help            show this help message and exit
  -e, --eeprom          Print content of the PLL configuration EEPROM
  -P {0,1}, --program {0,1}
                        Program PLL EEPROM page

Without any option: print PLL current configuration registers
```

### Initial PLL EEPROM Programming

When the module is powered on the PLL loads its configuration by
default from the EEPROM Page 0. This default configuration does
not enable PLL I2C interface, therefore, the configuration cannot
be changed. To make the PLL accessible via the I2C-bus it
should be configured from the factory programmed configuration in the
EEPROM Page 1. This can be done by providing a command line option `-p 1`
to the `gmm7550` utility.

When PLL is accessible via I2C-bus, its EEPROM Page 0
may be reprogrammed with the configuration that enables I2C and set
the clock parameters for the GMM-7550 module. This command should be
run once (at first power-up) on the module with the factory-default
configuration in the PLL EEPROM:

```
# gmm7550 -p 1 pll -P 0
```

After this command the PLL is configured to provide 100 MHz
differential clock to the FPGA and to be accessible on the I2C-bus by
default. The `-p 1` option is not required on subsequent runs of
the `gmm7550` command.

## Known Problems and Limitations

PLL EEPROM programming does not work on the VisionFive board.
