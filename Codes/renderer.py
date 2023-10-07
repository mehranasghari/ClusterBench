import os
import subprocess
import json
import jq
import argparse
from datetime import datetime
import pytz

# Define pathes
grafana_config_file_path = "./../conf/Software/GrafanaConfig.json"
hosts_file_path = "./../conf/Deployments/Host-names/hosts.txt"

# import grafana config data from json file
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
width = grafana_config_data["picture_width"]
height = grafana_config_data["picture_height"]
tz = grafana_config_data["Time_zone"]

# Import hosts lists
with open (hosts_file_path, 'r') as file:
    all_hosts = file.readlines

# time environment
tehran_time_zone = pytz.timezone('Asia/Tehran')

# process on argumants
argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--Start", help="Start-time (Start-time for taking pictures)")
argParser.add_argument("-e", "--End", help="End-time (End-time for taking pictures)")
argParser.add_argument("-p", "--path", help="path (path to save pictures)")
args = argParser.parse_args()

start_date_time = args.Start
start_date_time = datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
start_date_time = tehran_time_zone.localize(start_date_time)
start_utc_datetime = start_date_time.astimezone(pytz.UTC)
start_timestamp = start_utc_datetime.timestamp()
print (start_timestamp)

End_date_time = args.End
End_date_time = datetime.strptime(End_date_time, '%Y-%m-%d %H:%M:%S')
End_date_time = tehran_time_zone.localize(End_date_time)
end_utc_datetime = End_date_time.astimezone(pytz.UTC)
end_timestamp = end_utc_datetime.timestamp()
print (end_timestamp)

save_path = args.path if args.path else "./Pictures"

# Start renderring
def renderer(address, port, uid, dashboard_name, org_id, timeVariable, DataSource, start_timestamp, end_timestamp, width, height, all_hosts, save_path, tz):
    try:
        for host in all_hosts:
            host = host.strip().spilt(',')
            if len(host) >= 4:
                host = host[3].strip()
                i = 0
                # Recive panles id from grafana
                id_curl_command = f"curl -s -H \"Authorization: Bearer {key}\" \
                -H \"Content-Type: application/json\" \
                -X GET http://{address}:{port}/api/dashboards/uid/{uid} | jq '.dashboard.panels[] | .id'"                    
                ids_result = os.popen(id_curl_command).read()
                panel_ids = ids_result.strip().split("\n")

                # Recive panels name from grafana
                name_curl_command = f"curl -s -H \"Authorization: Bearer {key}\" \
                -H \"Content-Type: application/json\" \
                -X GET http://{address}:{port}/api/dashboards/uid/{uid} | jq '.dashboard.panels[].title' "                     
                name_result = os.popen(name_curl_command).read()
                panel_names = name_result.strip().split("\n")
                for panel_id in panel_ids:

                    pix_curl_command = f"""curl -s -o {save_path}/{panel_names[0+i]}.png -H "Authorization: Bearer {key}" 'http://{address}:{port}/render/d-solo/{uid}/{dashboard_name}?orgId={org_id}&var-hostIs={host}&var-timeVariable={timeVariable}&var-DataSource={DataSource}&from={start_timestamp}&to={end_timestamp}&panelId={panel_id}&width={width}&height={height}&tz={tz}'"""
                    pix_curl_process = subprocess.run(pix_curl_command, shell=True)
                    curl_exit_code = pix_curl_process.returncode
                    if curl_exit_code == 0:
                        print("Success")
                    else:
                        print("Error")
                    i += 1
            else:
                print("Error, there is no host in the list")
    except Exception as e:
        print("Error, in try part")
        print(e)
renderer(address, port, uid, dashboard_name, org_id, timeVariable, DataSource, start_timestamp, end_timestamp, width, height, all_hosts, save_path, tz)
