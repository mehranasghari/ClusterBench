import os
import subprocess
import json

# Specify address to config files
address_file_path = "./../conf/address.json"
hosts_file_path = "./../Hosts/hosts-test.txt"
query_file_path = "./queries.txt"
grafana_token_file_path = "./../conf/Grafana_token.txt"
# Load the JSON data from the file and define addresses as a variable
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Secondry_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Secondary_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Secondary_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Secondary_influxdb_address_in_host']

def query_parser(grafana_token_file_path):
    with open (grafana_token_file_path, 'w') as file:
        token = file.read
    
    curl -H "Authorization: Bearer eyJrIjoiUkpqZUNDRUxVSkxXWXBJaTJoMDB6djdSR1dlczI0VDMiLCJuIjoidGVzdCBmb3IgY29kZSIsImlkIjoxfQ==" http://157.119.190.139:3000/api/dashboards/home