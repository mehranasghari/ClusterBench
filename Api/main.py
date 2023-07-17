import os
import json
import subprocess

# Specify the measurments file path
measurment_file_path = "./measurments.txt"

# Open measurments file and read it
with open(measurment_file_path, 'r') as file :
    measurments = file.read
    for measurment in measurments:
        print(measurment)

