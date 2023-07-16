import os
import subprocess
import json

# Specify address to config files
defaults_file_address = "./../conf/address.json"
grafana_config_address = "./../conf/Grafana_config.json"
hosts_file_path = "./../Hosts/hosts-test.txt"
query_file_path = "./queries.txt"

# Load the JSON data from the default.json file and define addresses as a variable
with open(defaults_file_address, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Secondry_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Secondary_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Secondary_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Secondary_influxdb_address_in_host']
DB_name = json_data['Primary_influxdb_DB_name']
# Load grafana config
with open(grafana_config_address,'r') as file:
    json_data = json.load(file)
grafana_ip = json_data['grafana_ip']
grafana_port = json_data['grafana_port']
token = json_data['grafana_api_key']

def query_parser(query_file_path):
    
    # Read queries and loop them
    with open (query_file_path, 'r') as file :
        lines = file.readlines()
        for line in lines:
            curl_command = f'curl -H "Authorization: Bearer {token}" "http://{grafana_ip}:{grafana_port}/api/datasources/proxy/1/query?db={DB_name}&q={line}"> /dev/null'
            curl_process = subprocess.run(curl_command,shell=True)
            exit_code = curl_process.returncode
            if exit_code == 0:
                print("done")
            else:
                print("undone")
            
query_parser(query_file_path)