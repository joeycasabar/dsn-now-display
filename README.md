# dsn-now-display
Python code and systemd service files for building a physical display for satellite communications on NASA's Deep Space Network (DSN).

Uses a 16x32 HUB75-compatible RGB matrix and the Adafruit RGB Matrix Bonnet: https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi

See requirements.txt for required python packages.

While efforts have been made to follow best practices, this code is provided as-is and has not been put through thorough testing. Use at your own risk!

- `full_demo.py` initializes the attached RGB matrix display and continusously loops through the satellites identified in dsn.xml, displaying a short animation showing its name and any uplink or downlink activity
- `dsn_util.py` contains helper functions e.g. for parsing the xml file or expanding certain abbreviated spacecraft identifiers
- `download_test.py` renames any existing dsn.xml file and fetches an updated list of satellites from the public endpoint provided by NASA

The dsn.xml file can be automatically updated so that the list of satellites remains up-to-date. Example systemd service files can be found in the `services` directory
