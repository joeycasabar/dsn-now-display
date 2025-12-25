#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

# 1. Open an existing image or create a new one
# Replace 'your_image.jpg' with your image file path
try:
    image = Image.open('your_image.jpg').convert("RGB") # Convert to RGB for saving as JPG
except FileNotFoundError:
    # If the image file doesn't exist, create a new blank one
    print("Image not found, creating a new green image instead.")
    image = Image.new("RGB", (16, 32), color = "black")
# 2. Create a drawing context (object)
draw = ImageDraw.Draw(image)

# 3. Define text properties
text_content = 'J\nW\nS\nT'
# Specify font and size (ensure you have a font file available, e.g., 'arial.ttf')
try:
    font = ImageFont.truetype('m5x7.ttf', 8)
except IOError:
    # Fallback to default font if the specified font is not found
    print("Font not found, using default font.")
    font = ImageFont.load_default()

# Define text color (RGB tuple for white)
text_color = (255, 255, 255)

# Define position (top-left corner coordinates)
# (x, y) = (10, 10) pixels from the top-left corner
position = (8, -10)

# 4. Draw the text on the image
bbox = draw.textbbox((0,0), text_content, font=font, anchor="ma", align="center", spacing=0)
text_height = bbox[3] - bbox[1]
print(f"Text height: {text_height}")
draw.multiline_text(position, text_content, fill=text_color, font=font, anchor="ma", align="center", spacing=0)
image = image.rotate(90,expand=True)
# 5. Save the resulting image

output_path = 'image_with_text.jpg'
image.save(output_path)
print(f"Image saved to {output_path}")

# Optional: Display the image (this might require specific system configurations)
image.show()
