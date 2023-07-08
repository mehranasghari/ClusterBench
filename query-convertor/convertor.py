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
query_file_path = "./data.json"
output_file_path = "./queries.txt"  # Specify the file path to write the queries


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

# Convert JSON to InfluxDB query
def convert_panel_json_to_influxdb_query(panel_json, host):
   
    # Load the JSON from file
    json_data = json.loads(panel_json)

    # Extract query information
    targets = json_data.get("targets", [])

    influxdb_queries = []

    # Process each query target
    for target in targets:
        measurement = target.get("measurement")
        tags = target.get("tags", [])

        # Construct the measurement and tags portion of the query
        measurement_query = f'"{measurement}"'

        tag_queries = []
        for tag in tags:
            tag_name = tag.get("key")
            tag_value = tag.get("value")
            tag_operator = tag.get("operator", "=")
            tag_query = f'("{tag_name}" {tag_operator} {tag_value})'
            tag_queries.append(tag_query)

        tags_query = " AND ".join(tag_queries)

        # Construct the complete InfluxDB query
        influxdb_query = f'SELECT mean("value") FROM {measurement_query} WHERE ("host" =~ /^{host}$/)' + " AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);"
        influxdb_queries.append(influxdb_query)

    return influxdb_queries


# Read panel JSON from file
with open(query_file_path, "r") as panel_file:
    panel_json = panel_file.read()

# Host definition
with open(hosts_file_path, "r") as file:
    hosts = file.readlines()  # Read the hosts from the file
    hosts = [host.strip() for host in hosts]  # Remove any whitespace characters from the end of each line

# Iterate over each host and execute code
for dir_backup in backup_dir_list:
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
    extract_command = f"tar -xf {directorypath}/{dir_backup}/*.tar.gz -C {directorypath}/{dir_backup}/backup/"
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
    restore_command = f"docker exec -it {Secondary_influxdb_container_name} influxd restore -portable {Secondry_influxdb_in_container_address}/{dir_backup}/backup/ >/dev/null"
    restore_process = subprocess.run(restore_command, shell=True)
    exit_code = restore_process.returncode
    if exit_code == 0:
        print("\033[92mFiles restored successfully.\033[0m")
        print()
    else:
        print("\033[91mRestore failed.\033[0m")
        print()
        break

    # Create csv dir
    os.makedirs(f"{directorypath}/{dir_backup}/csv", exist_ok=True)

    # Read time of backup from each directory
    time_file_path = f"{Secondary_influxdb_address_in_host}/{dir_backup}/info/time"
    with open(time_file_path, "r") as file:
        time_str = file.read().strip()
        time_values = time_str.split(",")
        start_time, end_time = time_values[0], time_values[1]
        start_time_query = calendar.timegm(
            datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
        end_time_query = calendar.timegm(
            datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000

    # Set up the InfluxDB connection
    group_by = 'time(10s)'
    host = 'localhost'
    port = 8086
    database = f'{Secondary_influxdb_DB_name}'
    client = InfluxDBClient(host=host, port=port, database=database)

    for host in hosts:
        # Convert JSON to InfluxDB query
        influxdb_queries = convert_panel_json_to_influxdb_query(panel_json, host)
        influxdb_query = "\n".join(influxdb_queries)
        query = influxdb_queries
        print (influxdb_queries)

        # Run the query by variables
        formatted_query = []
        for item in query:
            formatted_item = item.format(group_by=group_by, host=host, start_time_query=start_time_query, end_time_query=end_time_query)
            formatted_query.append(formatted_item)
            query_string = ''.join(formatted_query)
            print(query_string)

            result = client.query(influxdb_queries)


        # Save the query result to a file and clear the query result.tx with echoing "" to it.
        csv_address = f'{directorypath}/{dir_backup}/csv/{host}_first_output.csv'

        with open(csv_address, 'w') as file:
            for series in result:
                for point in series:
                    file.write(str(point) + '\n')

            print(f"CSV for {host} saved to {csv_address}")

