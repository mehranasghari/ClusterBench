import os
import subprocess
import json

grafana_config_file_path = "./../conf/Software/GrafanaConfig.json"

# import data from json file
with open (grafana_config_file_path, 'r') as file:
    grafana_config_data = json.load(file)
key = grafana_config_data["api_key"]
address = grafana_config_data["URL"]
port = grafana_config_data["port"]
uid = grafana_config_data["uid"]
dashboard_name = grafana_config_data["dashboard_name"]
start_time = "1696304493550" #should use backsup start time in utc and timestamp
end_time = "1696390893550"   #should use backsup start time in utc and timestamp
panl_id = "39"

curl_command = f"curl -o output.png -H \"Authorization: Bearer {key}\" \"http://{address}:{port}/render/d-solo/{uid}/{dashboard_name}?orgId={panel_id}&from={start_time}&to={end_time}1&panelId=39&width=1000&height=500&tz=Asia%2FTehran\""
curl_process = subprocess.run(curl_command, shell=True)
curl_exit_code = curl_process.returncode
if curl_exit_code == 0:
    print("Success")
else:
    print("Error")