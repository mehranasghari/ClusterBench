import xml.etree.ElementTree as ET
import copy
import os
import sys
import random
import string
import re

class bcolors:
    YELLOW = '\033[1;33m'
    END = '\033[0m'

# Define the static output directory one level above the current working directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "all-xml"))

# Function to generate a random prefix of length up to 10 characters from A to Z
def random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a random value in the XML content
def replace_oprefix(xml_content):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={random_prefix()}', xml_content)

def update_worker_counts(xml_file, max_workers_main1):
    with open(xml_file, "r") as file:
        xml_template = file.read()

    original_file_name = os.path.splitext(os.path.basename(xml_file))[0]

    workers_main1 = 1
    while workers_main1 <= max_workers_main1:
        workers_main2 = workers_main1 * 3

        tree = ET.ElementTree(ET.fromstring(xml_template))
        root = tree.getroot()
        
        # Replace oprefix with a random value
        xml_template = replace_oprefix(xml_template)

        for work in root.findall(".//work[@name='main1']"):
            work.set('workers', str(workers_main1))

        for work in root.findall(".//work[@name='main2']"):
            work.set('workers', str(workers_main2))

        updated_file_name = f"{original_file_name}-p{workers_main1}-g{workers_main2}.xml"
        updated_file_path = os.path.join(output_dir, updated_file_name)

        with open(updated_file_path, "w") as updated_file:
            # Convert the XML content to a string before writing it
            updated_file.write(ET.tostring(root, encoding="utf-8").decode("utf-8"))

        #print(f"XML configuration updated for main1={bcolors.YELLOW}{workers_main1}{bcolors.END} and main2={bcolors.YELLOW}{workers_main2}{bcolors.END} workers and saved to {updated_file_name}.")

        workers_main1 *= 2

    #print(f"All configurations have been generated in the '{output_dir}' directory.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [xml_file] [max_workers_main1]")
        sys.exit(1)

    xml_file_name = sys.argv[1]
    max_workers_main1 = int(sys.argv[2])

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    update_worker_counts(xml_file_name, max_workers_main1)
