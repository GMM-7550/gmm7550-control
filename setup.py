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
    scripts=['bin/gmm7550-start', 'bin/test-adm1177']
)
