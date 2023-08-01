import json
import os
import subprocess

# Define addresses file path
address_file_path = "./../conf/address.json"
measurements_file_path = "./exported-measurements.txt"
metric_file_path = "./measurement.txt"
output_file_path = "./metric.txt"
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
if exec_process_exit_code == 0:
    print("\033[92mMeasuements execute successfully.\033[0m")
else:
    print("\033[91mMeasuements execute Failed.\033[0m")

# Metric file generator
with open(measurements_file_path , "r") as file:
    measurements_line = file.readlines()
    with open(metric_file_path , "r") as file :
        metirc_lines = file.readlines()
        for line in metirc_lines :
            if line in measurements_line:
                print_command = f"echo {line} > {output_file_path}"
                print_process = subprocess.run(print_command, shell=True)
        print("done")
