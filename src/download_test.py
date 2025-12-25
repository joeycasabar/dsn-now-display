#!/usr/bin/env python3

import requests

url = "https://eyes.nasa.gov/dsn/data/dsn.xml" # Replace with your XML URL
response = requests.get(url)

# Ensure the request was successful
response.raise_for_status() 

# Open a local file in binary write mode ('wb') and save the content
with open('dsn.xml', 'wb') as file:
    file.write(response.content)

print(f"Successfully saved XML content to downloaded_feed.xml")
