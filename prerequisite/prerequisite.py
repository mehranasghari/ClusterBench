import os
import subprocess
import json

InfluxdbConfig_file_path = "./../conf/Software/InfluxdbConfig.json"
with open (InfluxdbConfig_file_path, 'r') as file:
    file_data = json.load(file)

default_influxdb_container_name = file_data["Main_influxdb_container_name"]
default_db_name = file_data["Main_influxdb_DB_name"]
default_rp_name = file_data["Main_influxdb_database_rp_name"]

# Print some info 
print("\n\n\n\n")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(" DO NOT USE influxDB after running this script for at least 2 HOURS ")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("\n\n\n\n")

# Give some neccessary argumants from input
monster_vm_name = input("Please enter your Monster machine name : ") # ssh copy id should be done or handel it anyway
monster_container_name = input("Please enter your Monster conatiner name in machine : ")
influxdb_container_name = input(f"Please enter your InfluxDB container name (Default : {default_influxdb_container_name}): ")
if influxdb_container_name == "":
    influxdb_container_name = default_influxdb_container_name
db_name = input (f"Please enter your database name (Default : {default_db_name}): ")
if db_name == "" :
    db_name = default_db_name
rp_name = input(f"Please enter your active retention policy name (Default : {default_rp_name}): ")
if rp_name == "" :
    rp_name = default_rp_name

# Install pip and it dependencies
# Install pip
pip_installer_command = "apt install python3-pip 1>&2 /dev/null"
pip_installer_process = subprocess.run(pip_installer_command, shell=True)
pip_installer_exit_code = pip_installer_process.returncode

# Upgrade pip
pip_updater_command = "pip3 install --upgrade pip 1>&2 /dev/null" 
pip_updater_process = pip_installer_process = subprocess.run(pip_updater_command, shell=True)
pip_updater_process_exit_code = pip_updater_process.returncode

# Install InfluxDB client
influxdb_client_installer_command = "pip install influxdb 1>72 /dev/null"
influxdb_client_installer_process = pip_installer_process = subprocess.run(influxdb_client_installer_command, shell=True)
influxdb_client_installer_process_exit_code = influxdb_client_installer_process.returncode

# Install pytz
pytz_installer_command = "pip install pytz 1>&2 /dev/null"
pytz_installer_process = subprocess.run(pytz_installer_command, shell=True)
pytz_installer_process_exit_code = pytz_installer_process.returncode

if pip_installer_exit_code & pip_updater_process_exit_code & influxdb_client_installer_process_exit_code & pytz_installer_process_exit_code == 0:
    print("\033[92all dependecies installed successfully\033[0m")

# Change rp part
policy_changer_command = f"docker exec -it {influxdb_container_name} influx -execute 'alter retention policy {rp_name} on {db_name} shard duration 1h default'"
policy_changer_process = subprocess.run(policy_changer_command, shell=True)
policy_changer_exit_code = policy_changer_process.returncode

# connect to the monster container and run exporter command
exoprt_command = "ssh {monster_name} docker exec -it {monster_container_name} "