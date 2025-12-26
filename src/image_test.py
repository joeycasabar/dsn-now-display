#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

import time
from random import randrange
from rgbmatrix import RGBMatrix, RGBMatrixOptions

V_SPACING = 2

TEXT_XPOS = 9

FAST_DELAY = 0.01
SLOW_DELAY = 0.2
SLOW_POS = 10

TEXT_BRIGHTNESS = 63

options = RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 16
options.cols = 32

matrix = RGBMatrix(options=options)

image = Image.new("RGB", (16, 32), color="green")

draw = ImageDraw.Draw(image)
draw.fontmode = '1'

input_string = "JWST"
text_content = '\n'.join(input_string)

# Specify font and size (ensure you have a font file available, e.g., 'arial.ttf')
try:
    font = ImageFont.truetype('hd44780.ttf', 6)
except IOError:
    # Fallback to default font if the specified font is not found
    print("Font not found, using default font.")
    font = ImageFont.load_default(size=8)

# Define text color (RGB tuple for white)
text_color = (TEXT_BRIGHTNESS, TEXT_BRIGHTNESS, TEXT_BRIGHTNESS)

# Define position (top-left corner coordinates)
# (x, y) = (10, 10) pixels from the top-left corner

# 4. Draw the text on the image
bbox = draw.textbbox((0, 0), text_content, font=font,
                     anchor="ma", align="center", spacing=V_SPACING)
text_height = bbox[3] - bbox[1]
print(f"Text height: {text_height}")
y_start = 33
y_end = -text_height
text_y = y_start
fast_pos = y_end + (32 - SLOW_POS)

next_text = time.time()

while True:
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
        if text_y < y_end:
            text_y = y_start
