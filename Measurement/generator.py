import json
import os
import subprocess

# Define addresses file path
address_file_path = "./../conf/address.json"
exported_measurements_file_path = "./all-measurements.txt"
selected_measurements_file_path = "./metric-filterer.txt"
output_file_path = "./metric.txt"
matching_lines = []

# Load data from address.json file
with open(address_file_path, 'r') as file:
    json_data = json.load(file)

influxdb_container_name = json_data["Primary_influxdb_container_name"]
db_name = json_data["Primary_influxdb_DB_name"]
db_port = json_data["Primary_influxdb_container_port"]
db_host = json_data["Priamry_influxdb_host_in_container"]

# Delete existing file if any
delete_command = f"rm -rf {exported_measurements_file_path} {output_file_path} > /dev/null"
delete_process = subprocess.run(delete_command, shell=True)
delete_exit_code = delete_process.returncode
if delete_exit_code == 0:
    print("\033[92mDeleting Existing Files Successfully.\033[0m")
else:
    print("\033[91mDeleting  Failed.\033[0m")

# execute to container and save the input into the all-measurement.txt file
exec_command = f"docker exec -it {influxdb_container_name} influx -host {db_host} -port {db_port} -database '{db_name}' -execute 'SHOW MEASUREMENTS' > {exported_measurements_file_path} "
exec_process = subprocess.run(exec_command, shell=True)
exec_exit_code = exec_process.returncode
if exec_exit_code == 0:
    print("\033[92mMeasurements Generated Successfully.\033[0m")
else:
    print("\033[91mGenerating Measurements Failed.\033[0m")

# Metric file generator
with open(exported_measurements_file_path, "r") as measurements_file:
    exported_measurements_lines = measurements_file.readlines()

with open(selected_measurements_file_path, "r") as metric_file:
    selected_measurements_lines = metric_file.readlines()

for select_line in selected_measurements_lines:
    for export_line in exported_measurements_lines:
        if select_line.strip() in export_line:
            matching_lines.append(export_line)

with open(output_file_path, "a") as output_file:
    output_file.writelines(matching_lines)

if output_file_path :
    print("\033[92mMetrics Genereted Successfully.\033[0m")
else : 
    print("\033[91mGenerating Metrics Failed.\033[0m")