# dsn-now-display
Python code and systemd service files for building a physical display for satellite communications on NASA's Deep Space Network (DSN).

Uses a [16x32 HUB75-compatible RGB matrix](https://www.adafruit.com/product/420) and the [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211).

- `full_demo.py` initializes the attached RGB matrix display and loops through the satellites identified in dsn.xml, displaying a short animation showing its name and any uplink or downlink activity
- `dsn_util.py` contains helper functions e.g. for parsing the xml file or expanding certain abbreviated spacecraft identifiers
- `download_xml.py` renames any existing dsn.xml file and fetches an updated list of satellites from the public endpoint provided by NASA. The dsn.xml file can be automatically updated so that the list of satellites remains up-to-date. Example systemd service files can be found in the `services` directory

While efforts have been made to follow best practices, this code is provided as-is and has not been put through thorough testing. Use at your own risk!

## Installation

1. Follow the instructions to install the matrix software using the automated script: https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/install-using-script
1. Then, follow the instructions to setup the python venv: https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/python-usage
1. With the venv active, install the remaining packages by running `pip install -r requirements.txt`
1. Copy the python files to the `rgbmatrix` directory created earlier
1. Copy the service files to the appropriate directory and enable them (see [services/README.md](services/README.md))
