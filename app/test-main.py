import sys
import subprocess
import generate_xml
import os
import time
import shutil
import csv

# Getting arguments from main.sh
# Arguments are: input file, default file and script file
input_file_path = sys.argv[1]
default_file_path = sys.argv[2]
script_file_path = sys.argv[3]

# Defining paths
cosbench_command = './../../cli.sh'
archive_path = './../../archive/'
result_path = './../result/'
pre_test_script_path = script_file_path 
backup_script_path = './../Backup/backup_script.py'
hosts_file_path = "./../conf/Deployments/Host-names/hosts.txt" # this address added
submit = 'submit'
max_pre_test_script_failure = 3

# Defining temporary path for generating xml config file
temp_output_path = './temp_output'
temp_output_xml_path = './temp_output.xml'

# Splitting input file to workloads 
input = open(input_file_path, "r")
lines = input.read().split('}')
workloads = len(lines)
workloads -= 1
workload_name = ""

for workload_number in range(workloads):
    try:
        # Create a temporary file and xml for each workload
        temp_output_file_path = temp_output_path + "_" + str(workload_number)
        temp_output_file_xml_path = temp_output_xml_path + "_" + str(workload_number)
        file = open(temp_output_file_path, "w")
        file.write(lines[workload_number])
        file.close()

        # Generate config.xml file
        generate_xml.convert_input_to_xml(temp_output_file_path, default_file_path, temp_output_file_xml_path)

        # Find the name of workload
        file = open(temp_output_file_path, 'r')
        every_line = file.readlines()
        for l in every_line:
            if '{' in l:
                workload_name = l.split('{')[0].strip().rstrip()

        # Execute the script before running the test
        print()
        print("Executing pre-test script ...")
        time.sleep(1)
        pre_test_script_failure_num = 0
        for i in range(max_pre_test_script_failure):
            pre_test_script = subprocess.run([pre_test_script_path, workload_name], shell=True)
            if pre_test_script.returncode == 0:
                print("Pre-test script executed successfully!")
                break
            else:
                print("Pre-test script executed with failure!")
                pre_test_script_failure_num += 1
            time.sleep(1)
        print()
        if pre_test_script_failure_num == 3:
            print("Maximum pre-test script failures reached. Skipping this workload.")
            continue  # Continue with the next workload if pre-test fails
        
        # Start workload
        print(f"Workload {workload_name} is running ...")
        workload_file_path = temp_output_file_xml_path
        result = subprocess.run(["bash", cosbench_command, submit, workload_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print()

        # Extract ID of workload
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if line.find("ID"):
                output_line = line
        workload_id = output_line.rsplit(maxsplit=1)[-1]

        # Generate archive file name of workload
        archive_file_name = workload_id + "-swift-sample"
        print(f"Workload ID is: {workload_id}")
        print()

        # Check every second if the workload is ended or not
        while True:
            archive_file_path = os.path.join(archive_path, archive_file_name)
            if os.path.exists(archive_file_path):
                break
            time.sleep(1)

        # Create result directory of workloads
        result_file_path = os.path.join(result_path, workload_name)
        
        if os.path.exists(result_file_path):
            result_file_tail = '_' + '1' + '_'
            result_file_path += result_file_tail
            while os.path.exists(result_file_path):
                splitted_result_file = result_file_path.split('_')
                repeat_number = int(splitted_result_file[-2]) + 1
                splitted_result_file[-2] = str(repeat_number)
                result_file_path = '_'.join(splitted_result_file)

        os.mkdir(result_file_path)
        final_workload_name = result_file_path.split('/')[-1]

        # Create and copy workload.log
        archive_log_file = os.path.join(archive_file_path, 'workload.log') 
        result_log_file = os.path.join(result_file_path, 'workload.log')
        shutil.copy2(archive_log_file, result_log_file)

        # Create and copy workload-config.xml
        archive_config_file = os.path.join(archive_file_path, 'workload-config.xml') 
        result_config_file = os.path.join(result_file_path, 'workload-config.xml')
        shutil.copy2(archive_config_file, result_config_file)

        # Create archive csv file
        archive_csv_path = os.path.join(archive_file_path, archive_file_name)
        archive_csv_path += ".csv"

        # Create result csv file
        result_csv_path = os.path.join(result_file_path, workload_name)
        result_csv_path += ".csv"

        # Copy csv file from archive to result directory
        shutil.copy2(archive_csv_path, result_csv_path)

        # Remove config.xml file
        os.remove(temp_output_file_path)
        os.remove(temp_output_file_xml_path)

        # Find start of first main and end of last main
        with open(result_csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            first_main_launching_time = None
            last_main_completed_time = None

            for row in reader:
                if row[0].endswith('main'):
                    if first_main_launching_time is None:
                        first_main_launching_time = row[21]
                        last_main_completed_time = row[24]

        # Write time of workload in time file
        time_file_path = os.path.join(result_file_path, 'time')
        time_file = open(time_file_path, "w")
        start_time = first_main_launching_time.split('@')[1].strip()
        end_time = last_main_completed_time.split('@')[1].strip()
        start_end_time = start_time + ',' + end_time
        time_file.write(start_end_time)
        time_file.close()

        # Start backup phase and its process
        print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START OF BACKUP FOR\033[92m {final_workload_name} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        # Add get-ring and get-conf to result dir
        Ring_address = f"{result_path}/{final_workload_name}/Ring_cluster/"
        os.makedirs(Ring_address, exist_ok=True)

        conf_address = f"{result_path}/{final_workload_name}/Config_cluster/"
        os.makedirs(conf_address, exist_ok=True)

        get_conf_command = f"python3 ./../Codes/get_conf.py -f {hosts_file_path}"
        get_conf_process = subprocess.run(get_conf_command, shell=True)

        get_ring_command = f"python3 ./../Codes/get_ring.py -f {hosts_file_path}"
        get_ring_process = subprocess.run(get_ring_command, shell=True)

        # Mv all *.conf from . to result
        ring_mv_command = f"mv *.conf {conf_address}"
        ring_mv_process = subprocess.run(ring_mv_command, shell=True)

        conf_mv_command = f"mv *.txt {Ring_address}"
        conf_mv_process = subprocess.run(conf_mv_command, shell=True)

        subprocess.call(['python3', backup_script_path, '-t', final_workload_name])

    except Exception as e:
        print(f"An error occurred for workload {workload_name}: {str(e)}")
        continue  # Continue with the next workload if an error occurs
