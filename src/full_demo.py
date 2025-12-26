#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

import time
from random import randrange
from rgbmatrix import RGBMatrix, RGBMatrixOptions

import xml.etree.ElementTree as ET
import dsn_util

filename = 'dsn.xml'

PATTERN_HEIGHT = 64
MATRIX_WIDTH = 32

LINE_BRIGHTNESS = 255

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

TEXT_BRIGHTNESS = 255

FADE_MULT = 16

options = RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 16
options.cols = 32

matrix = RGBMatrix(options=options)

image = Image.new("RGB", (16, 32), color="green")

draw = ImageDraw.Draw(image)
draw.fontmode = '1'

try:
    # 2. Parse the XML file
    tree = ET.parse(filename)
    # 3. Get the root element
    root = tree.getroot()

    curr_spacecraft = dsn_util.parse_tree(root)

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except ET.ParseError:
    print(
        f"Error: Could not parse the XML in '{filename}'. Check file format.")

try:
    font = ImageFont.truetype('hd44780.ttf', 6)
except IOError:
    # Fallback to default font if the specified font is not found
    print("Font not found, using default font.")
    font = ImageFont.load_default(size=8)

text_color = (TEXT_BRIGHTNESS, TEXT_BRIGHTNESS, TEXT_BRIGHTNESS)

while True:
    for sc in curr_spacecraft:

        show_downsignal = False
        show_upsignal = False

        abbr = sc["abbr"]
        if abbr == "DSN" or abbr == 'DSS':
            continue

        if 'downSignal' in sc:
            if sc["downSignal"] == "true":
                show_downsignal = True

        if 'upSignal' in sc:
            if sc["upSignal"] == "true":
                show_upsignal = True

        if show_downsignal == False and show_upsignal == False:
            continue

        input_string = dsn_util.expand_name(abbr)
        text_content = '\n'.join(input_string)

        bbox = draw.textbbox((0, 0), text_content, font=font,
                             anchor="ma", align="center", spacing=V_SPACING)
        text_height = bbox[3] - bbox[1]
        print(f"Name: {input_string}, Height: {text_height}")
        y_start = 33
        y_end = -text_height
        text_y = y_start
        fast_pos = y_end + (32 - SLOW_POS)

        next_text = time.time()

        while text_y > y_end:
            draw.rectangle((0, 0, 16, 32), fill='black')
            draw.multiline_text((TEXT_XPOS, text_y), text_content, fill=text_color,
                                font=font, anchor="ma", align="center", spacing=V_SPACING)
            rotated_image = image.rotate(270, expand=True)
            matrix.SetImage(rotated_image, unsafe=False)
            if time.time() > next_text:
                if text_y > SLOW_POS or text_y < fast_pos:
                    text_y -= 2
                    next_text = time.time() + FAST_DELAY
                else:
                    text_y -= 1
                    next_text = time.time() + SLOW_DELAY

        matrix.Clear()
        time.sleep(0.5)

        step = 0

        for step in range(0, 1+MATRIX_WIDTH+PATTERN_HEIGHT):
            # print(step)
            if step < 16:
                line_color = (step * FADE_MULT, step *
                              FADE_MULT, step * FADE_MULT)
            elif step > 81:
                line_color = ((97-step) * FADE_MULT, (97-step)
                              * FADE_MULT, (97-step) * FADE_MULT)
            else:
                line_color = (LINE_BRIGHTNESS,
                              LINE_BRIGHTNESS, LINE_BRIGHTNESS)
            draw.rectangle((0, 0, 16, 32), fill='black')
            if show_downsignal:
                draw.line([(x, y-(PATTERN_HEIGHT-step))
                           for (x, y) in DOWN_LINES], fill=line_color)
            if show_upsignal:
                draw.line([(x, y+(MATRIX_WIDTH-step))
                           for (x, y) in UP_LINES], fill=line_color)
            rotated_image = image.rotate(270, expand=True)
            matrix.SetImage(rotated_image, unsafe=False)
            time.sleep(0.05)

        matrix.Clear()
        time.sleep(0.5)
