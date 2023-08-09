import os
import subprocess
import json

InfluxdbConfig_file_path = "./../conf/Software/InfluxdbConfig.json"
with open (InfluxdbConfig_file_path, 'r') as file:
    file_data = json.load(file)

default_influxdb_container_name = file_data["Main_influxdb_container_name"]
default_db_name = file_data["Main_influxdb_DB_name"]
default_rp_name = file_data["Main_influxdb_database_rp_name"]

# Clear the Page
clear_command = "clear"
os.system(clear_command)

def print_attention_message():
    print("\033[93m\033[1m" + " *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print(" DO NOT USE influxDB after running this script for at least 2 HOURS ")
    print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("\033[0m")

# Call the function to print the attention message
print_attention_message()

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

# Clear the Page
clear_command = "clear"
os.system(clear_command)

# Call the function to print the attention message
print_attention_message()

# Install pip and it dependencies
# Install pip
pip_installer_command = "apt install python3-pip > /dev/null  2>&1"
pip_installer_process = subprocess.run(pip_installer_command, shell=True)
pip_installer_exit_code = pip_installer_process.returncode()

# Upgrade pip
pip_updater_command = "pip3 install --upgrade pip > /dev/null  2>&1" 
pip_updater_process = pip_installer_process = subprocess.run(pip_updater_command, shell=True)
pip_updater_process_exit_code = pip_updater_process.returncode()

# Install InfluxDB client
influxdb_client_installer_command = "pip install influxdb > /dev/null 2>&1"
influxdb_client_installer_process = pip_installer_process = subprocess.run(influxdb_client_installer_command, shell=True)
influxdb_client_installer_process_exit_code = influxdb_client_installer_process.returncode()

# Install pytz
pytz_installer_command = "pip install pytz > /dev/null  2>&1"
pytz_installer_process = subprocess.run(pytz_installer_command, shell=True)
pytz_installer_process_exit_code = pytz_installer_process.returncode()


if pip_installer_exit_code & pip_updater_process_exit_code & influxdb_client_installer_process_exit_code & pytz_installer_process_exit_code == 0:
   print("\033[92mAll dependencies installed successfully\033[0m")

# Change rp part
policy_changer_command = f"docker exec -it {influxdb_container_name} influx -execute 'alter retention policy {rp_name} on {db_name} shard duration 1h default'"
policy_changer_process = subprocess.run(policy_changer_command, shell=True)
policy_changer_exit_code = policy_changer_process.returncode()

# connect to the monster container and run exporter command
exoprt_command = f"ssh {monster_vm_name} docker exec -it {monster_container_name} docker exec -it {monster_container_name}  > /dev/null 2>&1"
export_process = subprocess.run(exoprt_command, shell=True)
exoprt_process_exit_code = export_process.returncode
if exoprt_process_exit_code == 0:
   print("\033[92mRing files exported Successfully\033[0m")
else:
    print("\033[91mExporting ring files failed.\033[0m")

