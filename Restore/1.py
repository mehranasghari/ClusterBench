import os
import shutil
import datetime
import os
import subprocess
import argparse
import subprocess
import calendar
import json
from influxdb import InfluxDBClient


# Specify address to config files
address_file_path = "./../conf/address.json"
hosts_file_path = "./../Hosts/hosts.txt"

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
    
    # Drop DB
    drop_command = f"docker exec -it {Secondary_influxdb_container_name} influx -execute 'drop database {Secondary_influxdb_DB_name}'"
    drop_process = subprocess.run(drop_command, shell=True)
    exit_code = drop_process.returncode
    if exit_code == 0:
      print(f"\033[92mDatabase {Secondary_influxdb_DB_name} successfully.\033[0m")
      print()
    else:
      print(f"\033[91mDropping {Secondary_influxdb_DB_name} failed.\033[0m")
      print()
      break

    # Extract the backup.tar.gz
    extract_command = f"tar -xf {directoryname}/{dir_backup}/*.tar.gz -C {directoryname}/{dir_backup}/backup/"
    extract_process = subprocess.run(extract_command, shell=True)
    exit_code = extract_process.returncode
    if exit_code == 0:
      print("\033[92mBackup extracted successfully.\033[0m")
      print()
    else:
      print("\033[91mExtraction failed.\033[0m")
      print()
      break

    # Restore on influxdb
    restore_command = f"docker exec -it {Secondary_influxdb_container_name} influxd restore -portable {directoryname}/{dir_backup}/backup/ >/dev/null"
    restore_process = subprocess.run(restore_command, shell=True)
    exit_code = restore_process.returncode
    if exit_code == 0:
     print("\033[92mFiles restored successfully.\033[0m")
     print()
    else:
     print("\033[91mRestore failed.\033[0m")
     print()  
     break

    # Create csv dir 
    mkdir_command = f"mkdir {directoryname}/{dir_backup}/csv"
    mkdir_process = subprocess.run(mkdir_command, shell=True)
    exit_code_mkdir = mkdir_process.returncode
