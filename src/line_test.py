#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

MATRIX_WIDTH = 32

LINE_BRIGHTNESS = 64

UP_LINES = [
    (1, 1),
    (16, 8),
    (1, 16),
    (16, 24),
    (1, 30)
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
    (12, 32)
]

line_color = (LINE_BRIGHTNESS, LINE_BRIGHTNESS, LINE_BRIGHTNESS)

options = RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 16
options.cols = MATRIX_WIDTH

matrix = RGBMatrix(options=options)

image = Image.new("RGB", (16, 32), color="black")
# 2. Create a drawing context (object)
draw = ImageDraw.Draw(image)

next_text = time.time()

step = 0

while True:
    print(step)
    draw.rectangle((0, 0, 16, 32), fill='black')
    draw.line([(x, y+(MATRIX_WIDTH-step))
              for (x, y) in DOWN_LINES], fill=line_color)
    draw.line([(x, y-(MATRIX_WIDTH-step))
               for (x, y) in UP_LINES], fill=line_color)
    rotated_image = image.rotate(270, expand=True)
    matrix.SetImage(rotated_image, unsafe=False)
    step = 0 if step >= 64 else step + 1
    time.sleep(0.1)
