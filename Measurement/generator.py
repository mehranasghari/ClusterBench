import json
import os

# Define addresses file path
address_file_path = "./../conf/address.json"
exported_measurements_file_path = "./exported-measurements.txt"
selected_measurements_file_path = "./measurement.txt"
output_file_path = "./metric.txt"
match_lines = []

# Load data from address.json file
with open(address_file_path, 'r') as file:
    json_data = json.load(file)

influxdb_container_name = json_data["Primary_influxdb_container_name"]
db_name = json_data["Primary_influxdb_DB_name"]
db_port = json_data["Primary_influxdb_container_port"]
db_host = json_data["Priamry_influxdb_host_in_container"]

# execute to container and save the input into the measurement.txt file
#exec_command = f"docker exec -it {influxdb_container_name} influx -host {db_host} -port {db_port} -database '{db_name}' -execute 'SHOW MEASUREMENTS' > {exported_measurements_file_path} "
#os.system(exec_command)
# Assuming the execution of the command was successful, no need to check the exit code here.

# Metric file generator
with open(exported_measurements_file_path, "r") as measurements_file:
    exported_measurements_lines = measurements_file.readlines()

with open(selected_measurements_file_path, "r") as metric_file:
    selected_measurements_lines = metric_file.readlines()

matching_lines = []

for select_line in selected_measurements_lines:
    for export_line in exported_measurements_lines:
        if select_line.strip() in export_line:
            matching_lines.append(export_line)

with open(output_file_path, "a") as output_file:
    output_file.writelines(matching_lines)