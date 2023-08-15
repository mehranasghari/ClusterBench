import os
import subprocess
import json

# Define Pathes
Ring_dir_path = "./../conf/Depolyments/Ring"
InfluxdbConfig_file_path = "./../conf/Software/InfluxdbConfig.json"
ring_file_excueter_file_path = "./ring_file_excuter.sh"
exported_measurements_file_path = "./../Measurement/all-measurements.txt"
mover_file_path = "./mover.sh"

# Load data from InfluxdbConfig json file
with open (InfluxdbConfig_file_path, 'r') as file:
    file_data = json.load(file)

default_influxdb_container_name = file_data["Main_influxdb_container_name"]
default_db_name = file_data["Main_influxdb_DB_name"]
default_rp_name = file_data["Main_influxdb_database_rp_name"]
db_port = file_data["Main_influxdb_container_port"]
db_host = file_data["Main_influxdb_host_in_container"]

# Deifne some functions
# Clear the Page
clear_command = "clear"
os.system(clear_command)

# Define attention message function
def print_attention_message():
    print("\033[93m\033[1m" + " *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print(" DO NOT USE influxDB after running this script for at least 2 HOURS ")
    print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("\033[0m")

# Call the function to print the attention message
print_attention_message()

# Give some neccessary argumants from input
mc_name = input("enter mc name (Default: mv) : ")
if mc_name == "" :
    mc_name = "mc"
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
os.system(clear_command)

# Call the function to print the attention message
print_attention_message()

# delete file if exists
del_command = "rm -rf ./ring_file_excuter.sh"
del_process = subprocess.run(del_command, shell=True)
del_exit_code = del_process.returncode

# handeling mover.sh
# Generate and complete ring-file-excuter.sh
with open(ring_file_excueter_file_path , 'a') as file:
    file.write("swift-ring-builder /rings/account.builder > /account.txt")
    file.write(f"\nswift-ring-builder /rings/object.builder > /object.txt")
    file.write(f"\nswift-ring-builder /rings/container.builder > /container.txt")

# Check if file generated successfully or not
with open(ring_file_excueter_file_path, 'r') as file:
    content = file.read()

if content.strip():
    print("\033[92mRing File Excuter Generated Successfully\033[0m")
else:
    print("\033[91mRing File Excuter Generating Failed.\033[0m")

# Install pip and it dependencies
# Install pip
pip_installer_command = "apt install python3-pip > /dev/null  2>&1"
pip_installer_process = subprocess.run(pip_installer_command, shell=True)
pip_installer_exit_code = pip_installer_process.returncode

# Upgrade pip
pip_updater_command = "pip3 install --upgrade pip > /dev/null  2>&1" 
pip_updater_process = pip_installer_process = subprocess.run(pip_updater_command, shell=True)
pip_updater_process_exit_code = pip_updater_process.returncode

# Install InfluxDB client
influxdb_client_installer_command = "pip install influxdb > /dev/null 2>&1"
influxdb_client_installer_process = pip_installer_process = subprocess.run(influxdb_client_installer_command, shell=True)
influxdb_client_installer_process_exit_code = influxdb_client_installer_process.returncode

# Install pytz
pytz_installer_command = "pip install pytz > /dev/null  2>&1"
pytz_installer_process = subprocess.run(pytz_installer_command, shell=True)
pytz_installer_process_exit_code = pytz_installer_process.returncode

# Check all exit codes and print output
if pip_installer_exit_code & pip_updater_process_exit_code & influxdb_client_installer_process_exit_code & pytz_installer_process_exit_code == 0:
   print("\033[92mAll dependencies installed successfully\033[0m")
elif pip_installer_exit_code == 1:
    print("\033[91mfailed in installing pip\033[0m")
elif pip_updater_process_exit_code == 1:
    print("\033[91mpip updateing failed\033[0m")
elif influxdb_client_installer_process_exit_code == 1:
    print("\033[91minstalling influxdb clinet failed\033[0m")
elif pytz_installer_process_exit_code == 1:
    print("\033[91mpytz installing failed\033[0m")

# Change rp part
policy_changer_command = f"docker exec -it {influxdb_container_name} influx -execute 'alter retention policy {default_rp_name} on {default_db_name} shard duration 1h default'"
policy_changer_process = subprocess.run(policy_changer_command, shell=True)
policy_changer_exit_code = policy_changer_process.returncode

# Export all-mesurments file
exec_command = f"docker exec -it {influxdb_container_name} influx -host {db_host} -port {db_port} -database '{default_db_name}' -execute 'SHOW MEASUREMENTS' > {exported_measurements_file_path}"
exec_process = subprocess.run(exec_command, shell=True)
exec_exit_code = exec_process.returncode
if exec_exit_code == 0:
    print("\033[92mMeasurements Generated Successfully.\033[0m")
else:
    print("\033[91mGenerating Measurements Failed.\033[0m")

# trasfer ring_file_excuter.sh to the monster vm
trasnfer_command = f"scp ./ring_file_excuter.sh {monster_vm_name}:/ > /dev/null 2>&1"
trasnfer_process = subprocess.run(trasnfer_command, shell=True)
trasnfer_exit_code = trasnfer_process.returncode
if trasnfer_exit_code == 0 :
        print("\033[92mring-file-excuter moved Successfully\033[0m")

# Delete mover if exists
mover_rm_command = f"rm -rf {mover_file_path}"
mover_rm_process = subprocess.run(mover_rm_command, shell=True)
mover_rm_exit_code = mover_rm_process.returncode
if mover_rm_exit_code == 0:
    print("\033[92mmover deleted Successfully\033[0m")

# Generate mover
with open(mover_file_path, 'w') as file :
    file.write(f"docker cp {monster_container_name}:/account.txt /account.txt")
    file.write(f"docker cp {monster_container_name}:/object.txt /object.txt")
    file.write(f"docker cp {monster_container_name}:/container.txt /container.txt")
    file.write(f"scp /account.txt /object.txt /container.txt {mc_name}:/")
# Transfer mover.sh to monster container
trasnfer2_command = f"scp ./mover.sh {monster_vm_name}:/ > /dev/null 2>&1"
trasnfer2_process = subprocess.run(trasnfer2_command, shell=True)
trasnfer2_exit_code = trasnfer2_process.returncode
if trasnfer2_exit_code == 0 :
            print("\033[92mmover moved Successfully\033[0m")

# cp file to monster container
docker_cp_command = f"ssh {monster_vm_name} docker cp /ring_file_excuter.sh {monster_container_name}:/ > /dev/null 2>&1"
docker_cp_process = subprocess.run(docker_cp_command, shell=True)
docker_cp_exit_code = docker_cp_process.returncode
if docker_cp_exit_code == 0:
    print("\033[92mring-exuter moved to container successfully\033[0m")

# excute the script
execute_command = f"ssh {monster_vm_name} docker exec -t storage \"bash /ring_file_excuter.sh\""
execute_process = subprocess.run(execute_command, shell=True)
execute_exit_code = execute_process.returncode
if execute_exit_code == 0:
    print("\033[92mring-file executed Successfully\033[0m")

# Run mover.sh
execute2_command = f"ssh {monster_vm_name} \"bash /mover.sh\""
execute2_process = subprocess.run(execute_command, shell=True)
execute2_exit_code = execute2_process.returncode
if execute2_exit_code == 1:
    print("\033[92mmover runned Successfully\033[0m")

# Mv to config file 
mv_command = f"mv /*.txt ./../conf/Deployments"
mv_process = subprocess.run(mv_command, shell=True)
mv_exit_code = mv_process.returncode
if mv_exit_code == 1 :
    print("mv error")

# check the exit codes and print out put
if trasnfer_exit_code & docker_cp_exit_code & execute_exit_code & mv_exit_code == 1:
    print("\033[92mRing Files excuted and moved to conf dir\033[0m")
else :
    print("failed")