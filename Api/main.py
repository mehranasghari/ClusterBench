import os
import json
import subprocess

# Temporary variable defenitaion
host = "localhost"
port = "8086"

# Specify the files path
measurment_file_path = "./measurments.txt"
DB_conf_file_path = "./../conf/address.json"
hosts_file_path = "./../Hosts/hosts-test.txt"
# Open address.json and read some value from that
with open(DB_conf_file_path, 'r') as file:
        json_data = json.load(file)
DB_name = json_data['Primary_influxdb_DB_name']    

# Open measurments file and read it
with open(measurment_file_path, 'r') as file :
    measurments = file.readlines()
    for measurment in measurments:
        with open(hosts_file_path,'r') as file:
             hosts = file.readlines
             for host in hosts:
                curl_command = f'curl -G 'http://{host}:{port}/query?pretty=true' --data-urlencode "db={DB_name}" --data-urlencode "q=SELECT mean("value") FROM "{measurment}" WHERE ("host" =~ /^{host}$/) AND time >= now() - 30s AND time <= now() GROUP BY time(10s) fill(none)"'
                curl_process = subprocess.run(curl_command, shell=True)
                curl_exit_code = curl_process.returncode()
                if curl_exit_code == 0:
                    print("done")
                else:
                    print("not done")
