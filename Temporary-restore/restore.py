import os
import subprocess
import argparse
import sys
import json

# Specify address to address.json file
address_file_path = "./../conf/Software/InfluxdbConfig.json"

# Load the JSON data from the file and define adresses as a variable 
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Backup_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Backup_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Backup_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Backup_influxdb_address_in_host']

# Process given directory name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--directoryname", help="Directory Name (Directory which contain *.tar,gz)")
args = argParser.parse_args()
directoryname = args.directoryname

print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START OF RESTORE FOR\033[92m {directoryname} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

# Drop database
drop_command = f"docker exec -it {Secondary_influxdb_container_name} influx -execute 'drop database {Secondary_influxdb_DB_name}'"
drop_process = subprocess.run(drop_command, shell=True)
exit_code = drop_process.returncode
if exit_code == 0:
   print(f"\033[92mDatabase {Secondary_influxdb_DB_name} successfully.\033[0m")
   print()
else:
   print(f"\033[91mDropping {Secondary_influxdb_DB_name} failed.\033[0m")
   print()

# Extract the backup.tar.gz
extract_command = f"tar -xf {Secondary_influxdb_address_in_host}/{directoryname}/*.tar.gz -C {Secondary_influxdb_address_in_host}/{directoryname}/backup/"
extract_process = subprocess.run(extract_command, shell=True)
exit_code = extract_process.returncode
if exit_code == 0:
   print("\033[92mBackup extracted successfully.\033[0m")
   print()
else:
   print("\033[91mExtraction failed.\033[0m")
   print() 

# Restore on influxdb
restore_command = f"docker exec -it {Secondary_influxdb_container_name} influxd restore -portable {Secondry_influxdb_in_container_address}/{directoryname}/backup/ >/dev/null"
restore_process = subprocess.run(restore_command, shell=True)
exit_code = restore_process.returncode
if exit_code == 0:
   print("\033[92mFiles restored successfully.\033[0m")
   print()
else:
   print("\033[91mRestore failed.\033[0m")
   print() 
print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END OF RESTORE FOR\033[92m {directoryname} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

