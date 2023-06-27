import os
import shutil
import datetime
import os
import subprocess
import argparse
import subprocess
import calendar
import json

# Specify address to config files
address_file_path = "./../conf/address.json"

# Load the JSON data from the file and define adresses as a variable 
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Secondry_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Secondary_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Secondary_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Secondary_influxdb_address_in_host']

# Process given directory name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--directoryname", help="Directory Name (Directory which contain backup directories)")
args = argParser.parse_args()
directoryname = args.directoryname
dir_list = os.listdir(directoryname)
if directoryname == "":
    directoryname = Secondary_influxdb_address_in_host
    
for dir_backup in dir_list:
    print(dir_backup)