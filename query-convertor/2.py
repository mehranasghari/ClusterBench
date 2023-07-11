from influxdb import InfluxDBClient
import json
import os
import datetime
import subprocess
import argparse
import calendar
import json
import pytz
from datetime import datetime


# Specify address to config files
address_file_path = "./../conf/address.json"
hosts_file_path = "./../Hosts/hosts-test.txt"

# Load the JSON data from the file and define addresses as a variable
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Secondry_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Secondary_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Secondary_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Secondary_influxdb_address_in_host']

# Process given directory name as an argument
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--directorypath", help="Directory path (Directory which contains backup directories)")
args = argParser.parse_args()
directorypath = args.directorypath
backup_dir_list = os.listdir(directorypath)

# iterate over hosts
with open(hosts_file_path, 'r') as file:
    hosts = file.readlines()  # Read the hosts from the file
    hosts = [host.strip() for host in hosts]  # Remove any whitespace characters from the end of each line
    
    for backup_dir in backup_dir_list:     

            # Drop DB
            drop_command = f"docker exec -it {Secondary_influxdb_container_name} influx -execute 'drop database {Secondary_influxdb_DB_name}'"
            drop_process = subprocess.run(drop_command, shell=True)
            exit_code = drop_process.returncode
            if exit_code == 0:
                print(f"\033[92mDatabase {Secondary_influxdb_DB_name} dropped successfully.\033[0m")
                print()
            else:
                print(f"\033[91mDropping {Secondary_influxdb_DB_name} failed.\033[0m")
                print()
                break

            # Extract the backup.tar.gz
            extract_command = f"tar -xf {directorypath}/{backup_dir}/*.tar.gz -C {directorypath}/{backup_dir}/backup/"
            extract_process = subprocess.run(extract_command, shell=True)
            exit_code = extract_process.returncode
            if exit_code == 0:
                print("\033[92mBackup extracted successfully.\033[0m")
                print()
            else:
                print("\033[91mExtraction failed.\033[0m")
                print()
                break

            # Restore on InfluxDB
            restore_command = f"docker exec -it {Secondary_influxdb_container_name} influxd restore -portable {Secondry_influxdb_in_container_address}/{backup_dir}/backup/ >/dev/null"
            restore_process = subprocess.run(restore_command, shell=True)
            exit_code = restore_process.returncode
            if exit_code == 0:
                print("\033[92mFiles restored successfully.\033[0m")
                print()
            else:
                print("\033[91mRestore failed.\033[0m")
                print()
                break

            # delete unttar files
            delete_command = f'rm -rf {directorypath}/{backup_dir}/backup/*'
            delete_process = subprocess.run(delete_command, shell=True)
            exit_code = delete_process.returncode            
            if exit_code == 0:
                print("\033[92mFiles deleted successfully.\033[0m")
                print()
            else:
                print("\033[91mDeleting failed.\033[0m")
                print()
                break

            # Create csv dir
            os.makedirs(f"{directorypath}/{backup_dir}/csv", exist_ok=True)

            # Read time of backup from each directory
            time_file_path = f"{Secondary_influxdb_address_in_host}/{backup_dir}/info/time"
            with open(time_file_path, "r") as file:
                time_str = file.read().strip()
                time_values = time_str.split(",")
                start_time, end_time = time_values[0], time_values[1]
                start_time_query = calendar.timegm(
                    datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
                end_time_query = calendar.timegm(
                    datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
            
            for host in hosts:
                continue

