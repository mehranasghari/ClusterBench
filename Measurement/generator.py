import json
import os
import subprocess

# Define addresses file path
address_file_path = "./../conf/address.json"
measurements_file_path = "./measurements.txt"

# Load data from address.json file
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
influxdb_container_name = json_data["Primary_influxdb_container_name"]
db_name = json_data["Primary_influxdb_DB_name"]
db_port = json_data["Primary_influxdb_container_port"]
db_host = json_data["Priamry_influxdb_host_in_container"]

# execute to container and save the input into the measurement.txt file
exec_command = f"docker exec -it {influxdb_container_name} influx -host {db_host} -port {db_port} -database '{db_name}' -execute 'SHOW MEASUREMENTS' > {measurements_file_path} "
exec_process = subprocess.run(exec_command, shell= True)
exec_process_exit_code = exec_process.returncode
print (exec_process_exit_code)