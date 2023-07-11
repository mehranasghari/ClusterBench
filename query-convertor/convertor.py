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

        with open(output_file_path, 'w') as file:
            file.write(influxdb_queries)