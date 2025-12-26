import xml.etree.ElementTree as ET
import time

import dsn_util

import json

runtime = int(time.time())

# 1. Specify the filename (use a full path if the file is not in the same directory)
filename = 'dsn.xml'

try:
    # 2. Parse the XML file
    tree = ET.parse(filename)
    # 3. Get the root element
    root = tree.getroot()

    xml_ts = dsn_util.get_ts_from_xml(filename)
    print(
        f"XML Timestamp: {xml_ts}, {runtime-xml_ts} seconds ago")

    curr_spacecraft = dsn_util.parse_tree(root)

    for sc in curr_spacecraft:
        print(json.dumps(sc, indent=4))

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except ET.ParseError:
    print(
        f"Error: Could not parse the XML in '{filename}'. Check file format.")
