#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

import time
from random import randrange
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import xml.etree.ElementTree as ET
import os

import dsn_util

filename = 'dsn.xml'

options = RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 16
options.cols = 32

matrix = RGBMatrix(options=options)

image = Image.new("RGB", (16, 32), color="green")

draw = ImageDraw.Draw(image)
draw.fontmode = '1'

text_color = (
    dsn_util.TEXT_BRIGHTNESS,
    dsn_util.TEXT_BRIGHTNESS,
    dsn_util.TEXT_BRIGHTNESS
)

next_update = time.time()

try:
    font = ImageFont.truetype('hd44780.ttf', 6)
except IOError:
    # Fallback to default font if the specified font is not found
    print("Font not found, using default font.")
    font = ImageFont.load_default(size=8)

while True:
    curr_time = time.time()
    if curr_time > next_update:
        tree = ET.parse(filename)

        root = tree.getroot()

        curr_spacecraft = dsn_util.parse_tree(root)
        next_update = dsn_util.find_next_5min_epoch()

    print(f"Spacecraft found: {len(curr_spacecraft)}")

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
                             anchor="ma", align="center", spacing=dsn_util.V_SPACING)
        text_height = bbox[3] - bbox[1]
        print(f"Name: {input_string}, Height: {text_height}")
        y_start = 33
        y_end = -text_height
        text_y = y_start
        fast_pos = y_end + (32 - dsn_util.SLOW_POS)

        next_text = time.time()

        while text_y > y_end:
            draw.rectangle((0, 0, 16, 32), fill='black')
            draw.multiline_text((dsn_util.TEXT_XPOS, text_y), text_content, fill=text_color,
                                font=font, anchor="ma", align="center", spacing=dsn_util.V_SPACING)
            rotated_image = image.rotate(270, expand=True)
            matrix.SetImage(rotated_image, unsafe=False)
            if time.time() > next_text:
                if text_y > dsn_util.SLOW_POS or text_y < fast_pos:
                    text_y -= 2
                    next_text = time.time() + dsn_util.FAST_DELAY
                else:
                    text_y -= 1
                    next_text = time.time() + dsn_util.SLOW_DELAY

        matrix.Clear()
        time.sleep(0.5)

        step = 0

        for step in range(0, 1+dsn_util.MATRIX_WIDTH+dsn_util.PATTERN_HEIGHT):
            # print(step)
            if step < dsn_util.FADE_LEN:
                line_color = (
                    step * dsn_util.FADE_MULT,
                    step * dsn_util.FADE_MULT,
                    step * dsn_util.FADE_MULT
                )
            elif step > dsn_util.STEP_MAX - dsn_util.FADE_LEN:
                line_color = (
                    (dsn_util.STEP_MAX - step) * dsn_util.FADE_MULT,
                    (dsn_util.STEP_MAX - step) * dsn_util.FADE_MULT,
                    (dsn_util.STEP_MAX - step) * dsn_util.FADE_MULT
                )
            else:
                line_color = (
                    dsn_util.LINE_BRIGHTNESS,
                    dsn_util.LINE_BRIGHTNESS,
                    dsn_util.LINE_BRIGHTNESS
                )
            draw.rectangle((0, 0, 16, 32), fill='black')
            if show_downsignal:
                draw.line([(x, y-(dsn_util.PATTERN_HEIGHT-step))
                           for (x, y) in dsn_util.DOWN_LINES], fill=line_color)
            if show_upsignal:
                draw.line([(x, y+(dsn_util.MATRIX_WIDTH-step))
                           for (x, y) in dsn_util.UP_LINES], fill=line_color)
            rotated_image = image.rotate(270, expand=True)
            matrix.SetImage(rotated_image, unsafe=False)
            time.sleep(0.05)

        matrix.Clear()
        time.sleep(0.5)
