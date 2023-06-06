import datetime
import os
import subprocess

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
            start_datetime, end_datetime = line.strip().split(",")
            start_date, start_time = start_datetime.split(" ")
            end_date, end_time = end_datetime.split(" ")

            # Delete 'Z' from the end of time
           # start_time = start_time.rstrip("Z")
           # end_time = end_time.rstrip("Z")

            # Convert to datetime objects
            start_datetime = datetime.datetime.strptime(start_date + " " + start_time, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(end_date + " " + end_time, "%Y-%m-%d %H:%M:%S")

            # Convert to standard format (time only)
            start_time_standard = start_datetime.strftime("%H:%M:%S")
            end_time_standard = end_datetime.strftime("%H:%M:%S")
            # Remove all ":" for backup file name
            final_time_start_backup = start_time_standard.replace(":", "")
            final_time_end_backup = end_time_standard.replace(":", "")
            # print("final_time_start_backup : " , final_time_start_backup)
            # print("final_time_end_backup" , final_time_end_backup)

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

            backup_dir = start_date_dir + "T" + final_time_start_backup + "_" + end_date_dir + "T" +final_time_end_backup
            backup_path = "/var/lib/influxdb/test-backup/" + backup_dir
            os.makedirs(backup_path, exist_ok=True)

            start_time_backup = start_date + "T" + final_time_start + "Z"
            end_time_backup = end_date + "T" + final_time_end + "Z"
            #print("start_time_backup:", start_time_backup)
            #print("end_time_backup:", end_time_backup)
            #print("Backup directory:", backup_path)
            #print()

            # Perform backup using influxd backup command
            backup_command = f"docker exec -it influxdb influxd backup -portable -start {start_time_backup} -end {end_time_backup} {backup_path} >/dev/null "
            backup_process = subprocess.run(backup_command, shell=True)
            exit_code = backup_process.returncode
            if exit_code == 0:
                print("\033[92mBackup successful.\033[0m")
            else:
                print("\033[91mBackup failed.\033[0m")
            print()

            # Tar all backup files in the directory
            tar_file_path = backup_path + ".tar.gz"
            tar_command = f"docker exec -it influxdb tar -czvf {tar_file_path} -C {backup_path} . > /dev/null"
            tar_process = subprocess.run(tar_command, shell=True)
            if tar_process.returncode == 0:
                print("\033[92mCompression successful.\033[0m")
            else:
                print("\033[91mCompression failed.\033[0m")
            print()

            # Delete backup directory
            delete_command = f"docker exec -it influxdb rm -rf {backup_path}"
            delete_process = subprocess.run(delete_command, shell=True)
            delete_check = delete_process.returncode
            if delete_process.returncode == 0:
                print("\033[92mDeleting Directory Completed successfully.\033[0m")
            else:
                print("\033[91mDeleting Directory failed.\033[0m")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*")

input_file = "input.txt"
process_input_file(input_file)
