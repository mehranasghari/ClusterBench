import os
import subprocess

# Print some info 
print("\n\n\n\n")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(" DO NOT USE influxDB after running this script for at least 2 HOURS ")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("\n\n\n\n")

# Give some neccessary argumants from input
monster_vm_name = input("Please enter your Monster machine name : ") # ssh copy id should be done or handel it anyway
monster_container_name = input("Please enter your Monster conatiner name in machine : ")
influxdb_container_name = input("Please enter your InfluxDB container name : ")
db_name = input ("\nPlease enter your database name : ")
rp_name = input("\nPlease enter your active retention policy name : ")


# Install pip and it dependencies
# Install pip
pip_installer_command = "apt install python3-pip"
pip_installer_process = subprocess.run(pip_installer_command, shell=True)
pip_installer_exit_code = pip_installer_process.returncode()

# Upgrade pip
pip_updater_command = "pip3 install --upgrade pip" 
pip_updater_process = pip_installer_process = subprocess.run(pip_updater_command, shell=True)
pip_updater_process_exit_code = pip_updater_process.returncode()

# Install InfluxDB client
influxdb_client_installer_command = "pip install influxdb"
influxdb_client_installer_process = pip_installer_process = subprocess.run(influxdb_client_installer_command, shell=True)
influxdb_client_installer_process_exit_code = influxdb_client_installer_process.returncode()

# Install pytz
pytz_installer_command = "pip install pytz"
pytz_installer_process = subprocess.run(pytz_installer_command, shell=True)
pytz_installer_process_exit_code = pytz_installer_process.returncode()

if pip_installer_exit_code & pip_updater_process_exit_code & influxdb_client_installer_process_exit_code & pytz_installer_process_exit_code == 1:
    print("all dependecies installed successfully")

# Change rp part
policy_changer_command = f"docker exec -it {influxdb_container_name} influx -execute 'alter retention policy {rp_name} on {db_name} shard duration 1h default'"
policy_changer_process = subprocess.run(policy_changer_command, shell=True)
policy_changer_exit_code = policy_changer_process.returncode()

# connect to the monster container and run exporter command
exoprt_command = "ssh {monster_name} docker exec -it {monster_container_name} "