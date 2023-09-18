import sys
import xml.etree.ElementTree as ET
import os
import random
import string
import re

class bcolors:
    YELLOW = '\033[1;33m'
    END = '\033[0m'

# Define the static output directory one level above the current working directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "all-xml"))

# Function to generate a random prefix of length up to 10 characters from A to Z
def generate_random_prefix():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 10)))

# Function to replace oprefix with a specified value in the XML content
def replace_oprefix(xml_content, oprefix_value):
    return re.sub(r'oprefix=[A-Za-z]+', f'oprefix={oprefix_value}', xml_content)

def generate_xml(xml_file, max_worker_count):
    with open(xml_file, "r") as file:
        xml_template = file.read()

    random_prefix_value = generate_random_prefix()

    tree = ET.ElementTree(ET.fromstring(xml_template))
    root = tree.getroot()

    main_workstage = root.find(".//workstage[@name='main']")
    main1_session = main_workstage.find("./work[@name='main1']")
    main2_session = main_workstage.find("./work[@name='main2']")
    main3_session = main_workstage.find("./work[@name='main3']")

    worker_count = 2
    while worker_count <= max_worker_count - 1:
        current_oprefix = generate_random_prefix()
       
        main1_session.set("workers", str(worker_count))
        main2_session.set("workers", str(worker_count))
        main3_session.set("workers", str(worker_count))
        main1_operation = main1_session.find(".//operation")
        main2_operation = main2_session.find(".//operation")
        main3_operation = main3_session.find(".//operation") 
  
        main1_operation.set("config", replace_oprefix(main1_operation.get("config"), current_oprefix))
        main2_operation.set("config", replace_oprefix(main2_operation.get("config"), current_oprefix))
        main3_operation.set("config", replace_oprefix(main3_operation.get("config"), current_oprefix))

         # Modify oprefix values outside of main1 and main2 with the same value
        for elem in root.iter():
            if elem.tag == 'work' and elem != main1_session and elem != main2_session and elem != main3_session:
                config = elem.get("config")
                if config:
                    config = replace_oprefix(config, current_oprefix)
                    elem.set("config", config)


        modified_xml_file = os.path.basename(xml_file).replace('.xml', f'-p{worker_count}-g{worker_count}-d{worker_count}.xml')
        modified_xml_path = os.path.join(output_dir, modified_xml_file)
        
        tree.write(modified_xml_path, encoding='utf-8', xml_declaration='<?xml version="1.0" encoding="UTF-8" ?>')

        worker_count *= 2

    main1_session.set("workers", str(max_worker_count - 1))
    main2_session.set("workers", str(max_worker_count - 1))
    main3_session.set("workers", str(max_worker_count - 1))
    current_oprefix = generate_random_prefix()
    main1_operation = main1_session.find(".//operation")
    main2_operation = main2_session.find(".//operation")
    main3_operation = main3_session.find(".//operation")

    main1_operation.set("config", replace_oprefix(main1_operation.get("config"), current_oprefix))
    main2_operation.set("config", replace_oprefix(main2_operation.get("config"), current_oprefix))
    main3_operation.set("config", replace_oprefix(main3_operation.get("config"), current_oprefix))
      
     # Modify oprefix values outside of main1 and main2 with the same value
    for elem in root.iter():
        if elem.tag == 'work' and elem != main1_session and elem != main2_session and elem != main3_session:
            config = elem.get("config")
            if config:
                config = replace_oprefix(config, current_oprefix)
                elem.set("config", config)
 
    modified_xml_file = os.path.basename(xml_file).replace('.xml', f'-p{max_worker_count - 1}-g{max_worker_count - 1}-d{max_worker_count - 1}.xml')
    modified_xml_path = os.path.join(output_dir, modified_xml_file)

    tree.write(modified_xml_path, encoding='utf-8', xml_declaration='<?xml version="1.0" encoding="UTF-8" ?>')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [xml_file] [max_worker_count]")
        sys.exit(1)

    xml_file_path = os.path.abspath(sys.argv[1])
    max_worker_count = int(sys.argv[2])

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    generate_xml(xml_file_path, max_worker_count)
    #print(f"{bcolors.YELLOW}Modified XML files generated{bcolors.END}")
