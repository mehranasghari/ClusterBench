import datetime
import datetime
import os
import subprocess
import argparse
import calendar
import sys
import json
import time

# Specify address to address.json file
influxdb_conf_file_path = "./conf/Software/InfluxdbConfig.json"

# Load the JSON data from the file and define adresses as a variable 
with open(influxdb_conf_file_path, 'r') as file:
    json_data = json.load(file)
Primary_influxdb_in_container_address = json_data['Main_influxdb_in_container_address']
Primary_influxdb_address_in_host = json_data['Main_influxdb_address_in_host']
Secondary_influxdb_address_in_host = json_data['Backup_influxdb_address_in_host']
Primary_influxdb_container_name = json_data['Main_influxdb_container_name']
Secondary_influxdb_container_name = json_data['Backup_influxdb_container_name']
Time_add_to_end_of_test = int(json_data['Time_add_to_end_of_test'])
Time_reduce_from_first_of_test = int(json_data['Time_reduce_from_first_of_test'])
Main_influxdb_DB_name = json_data['Main_influxdb_DB_name']
# Define the GMT+03:30 offset in seconds
gmt_offset_seconds = 3 * 3600 + 30 * 60

# Read the line from the file (assuming it's stored in a variable called 'line')
line = "2023-09-05 23:45:15,2023-09-06 00:55:20"

# Split the line by ","
start_datetime_str, end_datetime_str = line.strip().split(",")

# Convert start and end datetime strings to datetime objects
start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")

# Define the number of seconds to add
seconds_to_add = 300  # For example, add 1 hour (3600 seconds)

# Add the GMT+03:30 offset to both datetime objects
start_datetime_utc = start_datetime - datetime.timedelta(seconds=gmt_offset_seconds)
end_datetime_utc = end_datetime - datetime.timedelta(seconds=gmt_offset_seconds)

dir_start_datetime_utc = start_datetime - datetime.timedelta(seconds=gmt_offset_seconds)
dir_end_datetime_utc = end_datetime - datetime.timedelta(seconds=gmt_offset_seconds)

# Add the specified number of seconds to both datetime objects
start_datetime_utc -= datetime.timedelta(seconds=Time_reduce_from_first_of_test)
end_datetime_utc += datetime.timedelta(seconds=Time_add_to_end_of_test)

# Convert the UTC datetime objects back to strings
start_datetime_utc_str = start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
end_datetime_utc_str = end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")

# creating backup time format
backup_start_date , backup_start_time = start_datetime_utc_str.split(" ")
start_time_backup = backup_start_date+"T"+backup_start_time+"Z"
backup_end_date , backup_end_time = end_datetime_utc_str.split(" ")
end_time_backup = backup_end_date+"T"+backup_end_time+"Z"

# dir name creation
dir_start_datetime_utc_str = dir_start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
dir_end_datetime_utc_str = dir_end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
dir_start_date , dir_start_time = dir_start_datetime_utc_str.split(" ")
dir_start_date = dir_start_date[2:].replace("-","")
dir_start_time = dir_start_time.replace(":","")
dir_end_date , dir_end_time = dir_end_datetime_utc_str.split(" ")
dir_end_date = dir_end_date[2:].replace("-","")
dir_end_time = dir_end_time.replace(":","")
backup_dir_name = dir_start_date+"T"+dir_start_time+"_"+dir_end_date+"T"+dir_end_time