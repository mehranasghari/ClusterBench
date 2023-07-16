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

def query_parser(grafana_token_file_path,query_file_path):
    
    # Read api key
    with open (grafana_token_file_path, 'r') as file:
        token = file.read()
    
    # Read queries and loop them
    with open (query_file_path, 'r') as file :
        lines = file.readlines()
        for line in lines:
            curl_command = f'curl -H "Authorization: Bearer {token}" > /dev/null'
            curl_process = subprocess.run(curl_command,shell=True)
            exit_code = curl_process.returncode
            if exit_code == 0:
                print("done")
            else:
                print("undone")
            
query_parser(grafana_token_file_path,query_file_path)
    #curl -H "Authorization: Bearer eyJrIjoiUkpqZUNDRUxVSkxXWXBJaTJoMDB6djdSR1dlczI0VDMiLCJuIjoidGVzdCBmb3IgY29kZSIsImlkIjoxfQ==" http://157.119.190.139:3000/api/dashboards/home