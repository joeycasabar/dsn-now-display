import xml.etree.ElementTree as ET

PATTERN_HEIGHT = 64
MATRIX_WIDTH = 32

LINE_BRIGHTNESS = 255
TEXT_BRIGHTNESS = 255
FADE_MULT = 16

UP_LINES = [
    (1, 1),
    (16, 8),
    (1, 16),
    (16, 24),
    (1, 32),
    (16, 40),
    (1, 48),
    (16, 56),
    (1, 64)
]

DOWN_LINES = [
    (12, 1),
    (4, 4),
    (12, 7),
    (4, 10),
    (12, 13),
    (4, 16),
    (12, 19),
    (4, 22),
    (12, 25),
    (4, 28),
    (12, 31),
    (4, 34),
    (12, 37),
    (4, 40),
    (12, 43),
    (4, 46),
    (12, 49),
    (4, 52),
    (12, 55),
    (4, 58),
    (12, 61)
]

V_SPACING = 2
TEXT_XPOS = 9

FAST_DELAY = 0.01
SLOW_DELAY = 0.1
SLOW_POS = 10


def parse_tree(root):
    curr_spacecraft = []
    for dish in root.iter("dish"):
        for target in dish.iter("target"):
            spacecraft = {
                "abbr": target.attrib["name"],
                # "dish": dish.attrib["name"]
            }
            for downsignal in dish.iter("downSignal"):
                if downsignal.attrib["spacecraft"] == spacecraft["abbr"]:
                    spacecraft["downSignal"] = downsignal.attrib["active"]
                    # spacecraft["ds_rate"] = downsignal.attrib["dataRate"]
            for upsignal in dish.iter("upSignal"):
                if upsignal.attrib["spacecraft"] == spacecraft["abbr"]:
                    spacecraft["upSignal"] = upsignal.attrib["active"]
                    # spacecraft["us_rate"] = upsignal.attrib["dataRate"]
        curr_spacecraft.append(spacecraft)
    return curr_spacecraft


def get_ts_from_xml(filename):

    try:
        # 2. Parse the XML file
        tree = ET.parse(filename)
        # 3. Get the root element
        root = tree.getroot()

        print(f"Root tag: {root.tag}")

        for timestamp in root.iter('timestamp'):
            timestamp = int(timestamp.text) / 1000.0

        return timestamp

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except ET.ParseError:
        print(
            f"Error: Could not parse the XML in '{filename}'. Check file format.")


def expand_name(abbr):
    missions = {
        "VGR1": "VOYAGER1",
        "VGR2": "VOYAGER2",
        "STA": "STEREOA",
        "CHDR": "CHANDRA",
        "JNO": "JUNO",
        "NHPC": "NEWHORIZONS",
        "M01O": "MARSODYSSEY",
        "M20": "PERSEVERANCE",
        "MSL": "CURIOSITY",
        "MVN": "MAVEN",
        "ORX": "OSIRISREX"
    }
    if abbr in missions:
        return missions.get(abbr)
    else:
        return abbr
