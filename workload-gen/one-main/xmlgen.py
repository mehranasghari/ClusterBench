import sys
import xml.etree.ElementTree as ET
import os
import random
import string
import re

class bcolors:
    YELLOW = '\033[1;33m'
    END = '\033[0m'

# Define the output directory as an absolute path
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "all-xml"))

# Function to generate a random prefix of length up to 10 characters from A to Z
def random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a random value in the XML content
def replace_oprefix(xml_content):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={random_prefix()}', xml_content)

def update_worker_count(xml_file, new_worker_count):
    with open(xml_file, "r") as file:
        xml_template = file.read()

    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)

    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()

    main_workstage = root.find(".//workstage[@name='main']")
    main_work = main_workstage.find("./work")
    main_work.set('workers', str(new_worker_count))

    modified_xml_file = xml_file.replace('.xml', f'-w{new_worker_count}.xml')
    modified_xml_path = os.path.join(output_dir, os.path.basename(modified_xml_file))

    # Write the modified XML content back to the file
    tree.write(modified_xml_path, encoding='utf-8', xml_declaration='<?xml version="1.0" encoding="utf-8"?>')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [input.xml] [max_worker_count]")
        sys.exit(1)

    xml_file_path = os.path.abspath(sys.argv[1])  # Accept an absolute path to the XML file
    max_worker_count = int(sys.argv[2])

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    worker_counts = [2 ** i for i in range(int(max_worker_count.bit_length()))]

    for count in worker_counts:
        update_worker_count(xml_file_path, count)
        #print(f"Modified XML for {bcolors.YELLOW}{count}{bcolors.END} workers saved in {output_dir}.")

    #print("All modifications complete.")
