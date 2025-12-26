import xml.etree.ElementTree as ET
import time

import json

runtime = int(time.time())

# 1. Specify the filename (use a full path if the file is not in the same directory)
filename = 'dsn.xml'

try:
    # 2. Parse the XML file
    tree = ET.parse(filename)
    # 3. Get the root element
    root = tree.getroot()

    print(f"Root tag: {root.tag}")

    for timestamp in root.iter('timestamp'):
        xml_timestamp = int(timestamp.text)/1000
        print(
            f"XML Timestamp: {xml_timestamp}, {runtime-xml_timestamp} seconds ago")

    curr_spacecraft = []

    # 4. Iterate over child elements
    for dish in root.iter("dish"):
        for target in dish.iter("target"):
            curr_spacecraft.append({
                "abbr": target.attrib["name"],
                "dish": dish.attrib["name"]
            })
            for downsignal in dish.iter("downSignal"):
                if downsignal.attrib["spacecraft"] == curr_spacecraft[-1]["abbr"]:
                    curr_spacecraft[-1]["ds_active"] = downsignal.attrib["active"]
                    curr_spacecraft[-1]["ds_rate"] = downsignal.attrib["dataRate"]
            for upsignal in dish.iter("upSignal"):
                if upsignal.attrib["spacecraft"] == curr_spacecraft[-1]["abbr"]:
                    curr_spacecraft[-1]["us_active"] = upsignal.attrib["active"]
                    curr_spacecraft[-1]["us_rate"] = upsignal.attrib["dataRate"]

    for sc in curr_spacecraft:
        print(json.dumps(sc, indent=4))

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except ET.ParseError:
    print(
        f"Error: Could not parse the XML in '{filename}'. Check file format.")
