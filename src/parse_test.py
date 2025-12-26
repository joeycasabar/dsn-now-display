import xml.etree.ElementTree as ET

# 1. Specify the filename (use a full path if the file is not in the same directory)
filename = 'dsn.xml'

try:
    # 2. Parse the XML file
    tree = ET.parse(filename)
    # 3. Get the root element
    root = tree.getroot()

    print(f"Root tag: {root.tag}")

    # 4. Iterate over child elements
    for dish in root.iter('dish'):
        for target in dish.iter('target'):
            print(dish.attrib["name"], target.attrib["name"])
        # print(f"Tag: {child.tag}, Attributes: {child.attrib}")

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except ET.ParseError:
    print(f"Error: Could not parse the XML in '{filename}'. Check file format.")
