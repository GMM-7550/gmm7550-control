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

### Known Problems and Limitations

PLL EEPROM programming does not work on the VisionFive board.

## SPI NOR

The `spi` subcommand allows read/program/erase content  of
the SPI NOR chip on the module.

To access the SPI NOR chip on the GMM-7550 module the SPI multiplexer
control bit 1 should be set with common option `gmm7550 -s 2 spi ...`.

To access an SPI NOR chip on a memory extension module connected
to the GMM-7550 the FPGA on the module should be pre-configured
with an SPI bridge design (in an SPI Passive mode) -- this is done
automatically when `-M` (`--mem`) option is specified.  The FPGA
configuration file is selected based on the connector the memory
extension module is connected to: P1 -- west, P2 -- north, P3 -- east.

Complete commands to read SPI NOR IDs on the module and on the memory
extension module are below, followed by their output."

```
# gmm7550 -s 2 spi -i
V = 5.04 V,  I =     6 mA
SPI NOR address range for operation: 0x0..0x-1
V = 5.03 V,  I =   121 mA
SPI Device Info:
JEDEC ID
  manufacturer: 9d
   memory type: 60
      capacity: 16
UID: 00 50 32 57 32 35 32 00 0b 12 4d ff 01 01 ff ff
```

```
# gmm7550 --mode=spi_passive -s 1 spi --mem=east -i
V = 5.04 V,  I =     6 mA
SPI NOR address range for operation: 0x0..0x-1
V = 5.06 V,  I =    76 mA
SPI Device Info:
JEDEC ID
  manufacturer: 9d
   memory type: 60
      capacity: 18
UID: 00 50 33 45 36 36 37 00 15 11 34 ff 01 01 ff ff
```

```
# gmm7550 spi --help
usage: gmm7550 spi [-h] [-i] [-n] [-r] [-w] [-e] [-a {address|from,to}]
                   [-p {page|from,to}] [-s {sector|from,to}]
                   [-b {block|from,to}] [-B {block|from,to}] [-C]
                   [-M {east,west,north}] [-f FILE]

options:
  -h, --help            show this help message and exit
  -i, --info            Print SPI NOR device info
  -n, --dry-run         Print the commands that would be executed, but do not
                        execute write and erase operations
  -r, --read            Read SPI NOR page(s) to file
  -w, --write           Write data from file to SPI NOR starting from the
                        given page number
  -e, --erase           Erase SPI NOR page(s)
  -a {address|from,to}, --addr {address|from,to}
                        Use SPI NOR address or address range
  -p {page|from,to}, --page {page|from,to}
                        Use SPI NOR page or range of pages
  -s {sector|from,to}, --sector {sector|from,to}
                        Use SPI NOR sector or range of sectors
  -b {block|from,to}, --block32 {block|from,to}
                        Use SPI NOR block (32KiB) or range of blocks
  -B {block|from,to}, --block64 {block|from,to}
                        Use SPI NOR block (64KiB) or range of blocks
  -C, --chip            Use entire SPI NOR chip
  -M {east,west,north}, --mem {east,west,north}
                        Access SPI NOR on the memory add-on board
  -f FILE, --file FILE  Filename to read/write SPI NOR data
```
