import datetime
import os
import subprocess
import argparse
import subprocess
import calendar
import sys
import json

# Specify address to address.json file
address_file_path = "./../conf/address.json"

# Load the JSON data from the file and define adresses as a variable 
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Primary_influxdb_backup_file_address = json_data['Primary_influxdb_backup_file_address']
mc_main_directory_address = json_data['mc_main_directory_address']
Secondary_influxdb_address = json_data['Secondary_influxdb_address']

# Process given Test name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--testname", help="Test Name (Directory in Result/)")
args = argParser.parse_args()
testDirectory = args.testname
global testDirectory2
testDirectory2 = args.testname
input_file = "./../result/"+testDirectory+"/time"

print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START OF BACKUP FOR\033[92m {testDirectory} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

def read_values_from_file(file_path):
    values = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            values.extend(line.strip().split(","))
    return values

def process_input_file(file_path_input):
    # set config time in seconds manually
    x = 600
    y = 600

    with open(file_path_input, "r") as f:
        lines = f.readlines()
        for line in lines:
            
            # Split and process input time
            start_datetime, end_datetime = line.strip().split(",")
            start_date, start_time = start_datetime.split(" ")
            end_date, end_time = end_datetime.split(" ")

            # Convert to datetime objects
            start_datetime = datetime.datetime.strptime(start_date + " " + start_time, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(end_date + " " + end_time, "%Y-%m-%d %H:%M:%S")

            # Convert to standard format (time only)
            start_time_standard = start_datetime.strftime("%H:%M:%S")
            end_time_standard = end_datetime.strftime("%H:%M:%S")

            # Remove all ":" for backup file name
            final_time_start_backup = start_time_standard.replace(":", "")
            final_time_end_backup = end_time_standard.replace(":", "")

            # Chnage time to UTC and verify the 10m time change
            final_time_end = (end_datetime + datetime.timedelta(seconds=y)).strftime("%H:%M:%S")
            final_time_start = (start_datetime - datetime.timedelta(seconds=x)).strftime("%H:%M:%S")

            # Remove all ":" for directory name
            final_time_start_dir = final_time_start.replace(":", "")
            final_time_end_dir = final_time_end.replace(":", "")

            # Remove all "-" for directory name
            start_date_dir = start_date.replace("-", "")
            start_date_dir = start_date_dir[2:]
            end_date_dir = end_date.replace("-", "")
            end_date_dir = end_date_dir[2:]

            # Create backup directory name structure
            backup_dir_name = start_date_dir + "T" + final_time_start_backup + "_" + end_date_dir + "T" +final_time_end_backup
            backup_path2 = Primary_influxdb_backup_file_address +"/"+ backup_dir_name
            backup_path = f"{Primary_influxdb_backup_file_address}/{backup_dir_name}" 
            os.makedirs(backup_path, exist_ok=True)
            start_time_backup = start_date + "T" + final_time_start + "Z"
            end_time_backup = end_date + "T" + final_time_end + "Z"

            # Perform backup using influxd backup command
            backup_command = f"docker exec -it influxdb influxd backup -portable -start {start_time_backup} -end {end_time_backup} {backup_path2}/backup >/dev/null "
            backup_process = subprocess.run(backup_command, shell=True)
            exit_code = backup_process.returncode
            if exit_code == 0:
                print("\033[92mBackup successful.\033[0m")
            else:
                print("\033[91mBackup failed.\033[0m")
                sys.exit(1)
            print()

            # Tar backup files and delete extra files
            tar_command = f"tar -cf {mc_main_directory_address}/{backup_dir_name}/backup.tar.gz -C {mc_main_directory_address}/{backup_dir_name}/backup {mc_main_directory_address}/{backup_dir_name} > /dev/null"
            tar_process = subprocess.run(tar_command, shell=True)
            exit_code = tar_process.returncode
            if exit_code == 0:
                print("\033[92mTar successful.\033[0m")
            else:
                print("\033[91mTar failed.\033[0m")
                sys.exit(1)
                print()
            
            # Delete backup directory files
            del_command = f"rm -rf {mc_main_directory_address}/{backup_dir_name}/backup/*"
            del_process = subprocess.run(del_command , shell=True)

            # Make info directory and move all into influxdb2 mount point
            os.makedirs(f"{mc_main_directory_address}/{backup_dir_name}/info", exist_ok=True)
            cp_command = f"cp -r ./../result/{testDirectory}/* {mc_main_directory_address}/{backup_dir_name}/info/"
            cp_process = subprocess.run(cp_command, shell=True)

	        #MV BACKUP.TAR.GZ TO influxdb2 and delete original file
            os.makedirs(Secondary_influxdb_address, exist_ok=True)
            mv_command = f"mv -f {mc_main_directory_address}/*  {Secondary_influxdb_address}/"
            mv_process = subprocess.run(mv_command, shell=True)
            exit_code = mv_process.returncode
            if exit_code == 0:
                print("\033[92mFiles moved to influxdb2 location successfully.\033[0m")
            else:
                print("\033[91mMoving files failed.\033[0m")
                sys.exit(1)
                print()
process_input_file(input_file)
print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END OF BACKUP FOR\033[92m {testDirectory} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
