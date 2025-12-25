#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

import time
from random import randrange
from rgbmatrix import RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 16
options.cols = 32

matrix = RGBMatrix(options = options)

image = Image.new("RGB", (16, 32), color = "green")

draw = ImageDraw.Draw(image)
draw.fontmode='1'

text_content = 'J\nW\nS\nT'
# Specify font and size (ensure you have a font file available, e.g., 'arial.ttf')
try:
    font = ImageFont.truetype('m5x7.ttf', 12)
except IOError:
    # Fallback to default font if the specified font is not found
    print("Font not found, using default font.")
    font = ImageFont.load_default()

# Define text color (RGB tuple for white)
text_color = (255, 255, 255)

# Define position (top-left corner coordinates)
# (x, y) = (10, 10) pixels from the top-left corner

# 4. Draw the text on the image
bbox = draw.textbbox((0,0), text_content, font=font, anchor="ma", align="center", spacing=0)
text_height = bbox[3] - bbox[1]
print(f"Text height: {text_height}")

while True:
    for y_pos in range(33, -text_height, -1):
        print(f"current y pos: {y_pos}")
        draw.rectangle((0,0,16,32), fill='black')
        draw.multiline_text((9, y_pos), text_content, fill=text_color, font=font, anchor="ma", align="center", spacing=0)
        rotated_image = image.rotate(90, expand=True)
        # matrix.Clear()
        matrix.SetImage(rotated_image, unsafe=False)
        # output_path = 'ypos_' + str(y_pos) + '.jpg'
        # rotated_image.save(output_path)
        time.sleep(0.01)