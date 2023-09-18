import re
import sys
import os
import random
import string

# Function to generate a random prefix of length up to 10 characters from A to Z
def random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a random value in the XML content
def replace_oprefix(xml_content, oprefix):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={oprefix}', xml_content)

# Check for command-line arguments
if len(sys.argv) != 3:
    print("Usage: script.py <path_to_xml_file> <max_size>")
    sys.exit(1)

# Get the path to the XML file and the maximum size from command-line arguments
xml_path = sys.argv[1]
max_size = int(sys.argv[2])

# Read the template XML file
with open(xml_path, "r") as file:
    xml_template = file.read()

# Create a directory to store the output XML files in the current directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "all-xml"))
os.makedirs(output_dir, exist_ok=True)

# Start with size as 1 and double it until it exceeds the specified maximum size
size = 1
while size <= max_size:
    # Generate a new random oprefix for each file
    oprefix = random_prefix()
    
    # Replace oprefix in the XML content with the random oprefix
    xml_template = replace_oprefix(xml_template, oprefix)
    
    # Replace sizes in the XML content
    xml_content = re.sub(r'sizes=c\(\d+\)KB', f'sizes=c({size})KB', xml_template)
    
    # Write the modified XML content to a new file in the "all-xml" directory
    output_file_name = f"{os.path.splitext(os.path.basename(xml_path))[0]}-sizes-{size}.xml"
    output_file_path = os.path.join(output_dir, output_file_name)
    with open(output_file_path, "w") as file:
        file.write(xml_content)
    
    # Double the size for the next iteration
    size *= 2

#print(f"XML templates with sizes in powers of 2 and unique random oprefix values have been created in the '{output_dir}' directory.")
