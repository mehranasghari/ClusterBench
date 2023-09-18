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

# Function to generate a random prefix of length up to 10 characters from A to Z
def random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a random value in the XML content
def replace_oprefix(xml_content):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={random_prefix()}', xml_content)

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <xml_file> <max_workers>")
    exit(1)

# Get the XML file path and maximum number of workers from command-line arguments
xml_file_path = sys.argv[1]
try:
    max_workers = int(sys.argv[2])
except ValueError:
    print("Invalid input for max_workers. Please provide a valid number.")
    exit(1)

# Normalize the XML file path to an absolute path
xml_file_path = os.path.abspath(xml_file_path)

# Get the directory containing the XML file
xml_file_directory = os.path.dirname(xml_file_path)

# Define the output directory for saving the files (one level above the XML file directory)
output_directory = os.path.abspath(os.path.join(xml_file_directory, os.pardir, "all-xml"))

# Ensure the output directory exists, or create it if it doesn't
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(xml_file_path, "r") as file:
    xml_template = file.read()

# Parse the XML configuration file
try:
    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()
except FileNotFoundError:
    print("File not found. Please provide a valid XML file path.")
    exit(1)
except ET.ParseError:
    print("Invalid XML file. Please provide a valid XML file.")
    exit(1)

# Extract the original XML file name (without extension)
original_file_name = os.path.splitext(os.path.basename(xml_file_path))[0]

# Define the three scenarios
scenarios = [
    {"main1_range": True, "main2_range": False, "main3_range": False},
    {"main1_range": False, "main2_range": True, "main3_range": False},
    {"main1_range": False, "main2_range": False, "main3_range": True}
]

# Function to generate a list of numbers counting in doubles up to max_value
def generate_doubles(max_value):
    num = 1
    doubles = [1]
    while num < max_value:
        num *= 2
        if num <= max_value:
            doubles.append(num)
    return doubles
 
for i, scenario in enumerate(scenarios, start=1):
    main1_range = scenario["main1_range"]
    main2_range = scenario["main2_range"]
    main3_range = scenario["main3_range"]

    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()

    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)


    # Generate a list of worker values counting in doubles
    worker_values = generate_doubles(max_workers)

    for workers in worker_values:
        # Create a deep copy of the root element for each iteration
        new_root = copy.deepcopy(root)
        
        tree = ET.ElementTree(ET.fromstring(xml_template))
        root = tree.getroot()

        # Replace oprefix with a random value
        xml_template = replace_oprefix(xml_template)

        # Find and update the number of workers in main1
        for work in new_root.findall(".//work[@name='main1']"):
            if main1_range:
                work.set('workers', str(workers))
            else:
                work.set('workers', '1')

        # Find and update the number of workers in main2
        for work in new_root.findall(".//work[@name='main2']"):
            if main2_range:
                work.set('workers', str(workers))
            else:
                work.set('workers', '1')

        # Find and update the number of workers in main3
        for work in new_root.findall(".//work[@name='main3']"):
            if main3_range:
                work.set('workers', str(workers))
            else:
                work.set('workers', '1')

        # Generate a new XML file name based on the specified format
        if i == 1:
            updated_file_name = f"{original_file_name}-type{i}-p{workers}-g1-d1.xml"
        elif i == 2:
            updated_file_name = f"{original_file_name}-type{i}-p1-g{workers}-d1.xml"
        elif i == 3:
            updated_file_name = f"{original_file_name}-type{i}-p1-g1-d{workers}.xml"

        # Define the path to save the updated XML file in the output directory
        updated_file_path = os.path.join(output_directory, updated_file_name)

        # Save the updated XML to a new file
        tree_copy = ET.ElementTree(new_root)
        tree_copy.write(updated_file_path)

        #print(f"Type{bcolors.YELLOW}{i}{bcolors.END}: XML configuration generated {bcolors.YELLOW}{updated_file_name}{bcolors.END}")

#print("All configurations have been generated.")
