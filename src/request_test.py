#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET

def fetch_and_parse_xml(url):
    """
    Fetches an XML feed using requests and parses it with ElementTree.
    """
    # 1. Send the HTTP Request
    try:
        response = requests.get(url, headers={'Accept': 'application/xml'})
        response.raise_for_status() # Raise an exception for bad status codes (4XX or 5XX)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    # 2. Access the Content
    xml_data = response.content # Use .content for binary write, .text for string if encoding is fine

    # 3. Parse the XML String
    try:
        root = ET.fromstring(xml_data)
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

# Example Usage:
# Replace with a valid XML URL
xml_url = 'https://eyes.nasa.gov/dsn/data/dsn.xml'
root_element = fetch_and_parse_xml(xml_url)

if root_element is not None:
    print(f"Root tag: {root_element.tag}")
    # Loop through elements (example: printing titles from an RSS feed)
    for item in root_element:
        print(item.tag, item.attrib)
        for child in item:
            print(child)

