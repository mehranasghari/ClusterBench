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

# Get the path of the script itself
script_path = os.path.abspath(__file__)

# Calculate the parent directory of the script
parent_directory = os.path.abspath(os.path.join(script_path, os.pardir))

# Function to generate a random prefix of length up to 10 characters from A to Z
def random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a random value in the XML content
def replace_oprefix(xml_content):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={random_prefix()}', xml_content)

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <xml_file> <max_number>")
    exit(1)

# Get the XML file path and maximum number from command-line arguments
xml_file_path = os.path.abspath(sys.argv[1])
try:
    max_number = int(sys.argv[2])
except ValueError:
    print("Invalid input for max_number. Please provide a valid number.")
    exit(1)

# Define the directory for saving output files (one level above the script directory)
output_directory = os.path.join(parent_directory,"..", "all-xml")

# Ensure the output directory exists, or create it if it doesn't
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(xml_file_path, "r") as file:
    xml_template = file.read()

# Parse the XML configuration file
try:
    #tree = ET.parse(xml_file_path)
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

# Initialize the worker count for "main1" and "main2" to 1
workers_main1 = 1
workers_main2 = 1

# Create a set to store unique worker count combinations
unique_combinations = set()

# Create XML files with "main1" having a static 1 and "main2" in a range, counting in double (Type 1)
while workers_main2 <= max_number:
    # Create a deep copy of the root element for each iteration
    new_root = copy.deepcopy(root)
    
    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()
        
    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)

    # Find and update the number of workers in main1 (static 1)
    for work in new_root.findall(".//work[@name='main1']"):
        work.set('workers', '1')
    
    # Find and update the number of workers in main2 (range, counting in double)
    for work in new_root.findall(".//work[@name='main2']"):
        work.set('workers', str(workers_main2))
    
    # Generate a new XML file name based on the specified format
    updated_file_name = f"{original_file_name}-type1-p1-g{workers_main2}.xml"
    
    # Check if the combination has already been processed
    combination = (1, workers_main2)
    if combination not in unique_combinations:
        unique_combinations.add(combination)
        
        # Save the updated XML to the output directory
        updated_file_path = os.path.join(output_directory, updated_file_name)
        
        tree_copy = ET.ElementTree(new_root)
        tree_copy.write(updated_file_path)
        
        #print(f"Type 1: XML configuration updated for main1={bcolors.YELLOW}1{bcolors.END} and main2={bcolors.YELLOW}{workers_main2}{bcolors.END} workers and saved to {bcolors.YELLOW}{updated_file_name}{bcolors.END}")
    
    # Double the worker count for "main2" for the next iteration
    workers_main2 *= 2

# Reset worker counts
workers_main1 = 1
workers_main2 = 1

# Create XML files with "main2" having a static 1 and "main1" in a range, counting in double (Type 2)
while workers_main1 <= max_number:
    # Create a deep copy of the root element for each iteration
    new_root = copy.deepcopy(root)

    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()
    
    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)
 
    # Find and update the number of workers in main2 (static 1)
    for work in new_root.findall(".//work[@name='main2']"):
        work.set('workers', '1')
    
    # Find and update the number of workers in main1 (range, counting in double)
    for work in new_root.findall(".//work[@name='main1']"):
        work.set('workers', str(workers_main1))
    
    # Generate a new XML file name based on the specified format
    updated_file_name = f"{original_file_name}-type2-p{workers_main1}-g1.xml"
    
    # Check if the combination has already been processed
    combination = (workers_main1, 1)
    if combination not in unique_combinations:
        unique_combinations.add(combination)
        
        # Save the updated XML to the output directory
        updated_file_path = os.path.join(output_directory, updated_file_name)
        
        tree_copy = ET.ElementTree(new_root)
        tree_copy.write(updated_file_path)
        
        #print(f"Type 2: XML configuration updated for main1={bcolors.YELLOW}{workers_main1}{bcolors.END} and main2={bcolors.YELLOW}1{bcolors.END} workers and saved to {bcolors.YELLOW}{updated_file_name}{bcolors.END}")
    
    # Double the worker count for "main1" for the next iteration
    workers_main1 *= 2

# Reset worker counts
workers_main1 = 1
workers_main2 = 1

# Create XML files with "main1" having the maximum number and "main2" in a range, counting in double (Type 3)
while workers_main2 <= max_number:
    # Create a deep copy of the root element for each iteration
    new_root = copy.deepcopy(root)
     
    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()
    
    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)

    # Find and update the number of workers in main1 (maximum)
    for work in new_root.findall(".//work[@name='main1']"):
        work.set('workers', str(max_number))
    
    # Find and update the number of workers in main2 (range, counting in double)
    for work in new_root.findall(".//work[@name='main2']"):
        work.set('workers', str(workers_main2))
    
    # Generate a new XML file name based on the specified format
    updated_file_name = f"{original_file_name}-type3-p{max_number}-g{workers_main2}.xml"
    
    # Check if the combination has already been processed
    combination = (max_number, workers_main2)
    if combination not in unique_combinations:
        unique_combinations.add(combination)
        
        # Save the updated XML to the output directory
        updated_file_path = os.path.join(output_directory, updated_file_name)
        
        tree_copy = ET.ElementTree(new_root)
        tree_copy.write(updated_file_path)
        
        #print(f"Type 3: XML configuration updated for main1={bcolors.YELLOW}{max_number}{bcolors.END} and main2={bcolors.YELLOW}{workers_main2}{bcolors.END} workers and saved to {bcolors.YELLOW}{updated_file_name}{bcolors.END}")
    
    # Double the worker count for "main2" for the next iteration
    workers_main2 *= 2

# Reset worker counts
workers_main1 = 1
workers_main2 = 1

# Create XML files with "main2" having the maximum number and "main1" in a range, counting in double (Type 4)
while workers_main1 <= max_number:
    # Create a deep copy of the root element for each iteration
    new_root = copy.deepcopy(root)

    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()
    
    # Replace oprefix with a random value
    xml_template = replace_oprefix(xml_template)

    # Find and update the number of workers in main2 (maximum)
    for work in new_root.findall(".//work[@name='main2']"):
        work.set('workers', str(max_number))
    
    # Find and update the number of workers in main1 (range, counting in double)
    for work in new_root.findall(".//work[@name='main1']"):
        work.set('workers', str(workers_main1))
    
    # Generate a new XML file name based on the specified format
    updated_file_name = f"{original_file_name}-type4-p{workers_main1}-g{max_number}.xml"
    
    # Check if the combination has already been processed
    combination = (workers_main1, max_number)
    if combination not in unique_combinations:
        unique_combinations.add(combination)
        
        # Save the updated XML to the output directory
        updated_file_path = os.path.join(output_directory, updated_file_name)
        
        tree_copy = ET.ElementTree(new_root)
        tree_copy.write(updated_file_path)
        
        #print(f"Type 4: XML configuration updated for main1={bcolors.YELLOW}{workers_main1}{bcolors.END} and main2={bcolors.YELLOW}{max_number}{bcolors.END} workers and saved to {bcolors.YELLOW}{updated_file_name}{bcolors.END}")
    
    # Double the worker count for "main1" for the next iteration
    workers_main1 *= 2

#print("All configurations have been generated.")
