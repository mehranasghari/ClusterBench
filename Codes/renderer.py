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
org_id = grafana_config_data["org_id"]
timeVariable = grafana_config_data["timeVariable"]
DataSource = grafana_config_data["DataSource"]
start_time = "1696304493550" #should use backsup start time in utc and timestamp
end_time = "1696390893550"   #should use backsup start time in utc and timestamp
panel_id = "39"

# Start renderring
def renderer(address, port, uid, dashboard_name, org_id, timeVariable, DataSource, start_time, end_time, panel_id):
    
    curl_command = f"curl -o output.png -H \"Authorization: Bearer {key}\" http://{address}:{port}/render/d-solo/{uid}/{dashboard_name}?orgId={org_id}&var-hostIs=m-r1z1s5-controller&var-timeVariable={timeVariable}&var-DataSource={DataSource}&from=1696399144231&to=1696400944231&panelId={panel_id}&width=1000&height=500&tz=Asia%2FTehran\""
    curl_process = subprocess.run(curl_command, shell=True)
    curl_exit_code = curl_process.returncode
    if curl_exit_code == 0:
        print("Success")
    else:
        print("Error")
        
renderer(address, port, uid, dashboard_name, org_id, timeVariable, DataSource, start_time, end_time, panel_id)
