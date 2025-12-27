#!/usr/bin/env python3

import requests
import dsn_util

import os

filename = 'dsn.xml'
url = "https://eyes.nasa.gov/dsn/data/dsn.xml"  # Replace with your XML URL
response = requests.get(url)

# Ensure the request was successful
response.raise_for_status()

try:
    xml_ts = f"{dsn_util.get_ts_from_xml(filename):.0f}"
    os.rename(filename, 'dsn_' + xml_ts + '.xml')

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
finally:
    # Open a local file in binary write mode ('wb') and save the content
    with open(filename, 'wb') as file:
        file.write(response.content)

    print(f"Successfully saved XML content to {filename}")
