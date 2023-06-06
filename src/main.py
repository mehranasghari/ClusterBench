import sys
import subprocess
import generate_xml
import os
import time
import shutil
import csv

script_path = './../../cli.sh'
output_path = './../../archive/'
result_path = './../result/'
submit = 'submit'

input_file = sys.argv[1]
default_file = sys.argv[2]
script_file = sys.argv[3]

temp_output_path = './temp_output'
temp_output_xml_path = './temp_output.xml'

input = open(input_file, "r")
lines = input.read().split('}')
workloads = len(lines)
workloads -= 1

workload_name = ""

for workload_number in range(workloads):
    temp_output_file = temp_output_path + "_" + str(workload_number)
    temp_output_file_xml = temp_output_xml_path + "_" + str(workload_number)
    file = open(temp_output_file, "w")
    file.write(lines[workload_number])
    file.close()
    generate_xml.convert_input_to_xml(temp_output_file, default_file, temp_output_file_xml)
    file = open(temp_output_file, 'r')
    every_line = file.readlines()
    for l in every_line:
        if '{' in l:
            workload_name = l.split('{')[0].strip().rstrip()
    print(f"Workload {workload_name} is running ...")
    workload_file = temp_output_file_xml
    result = subprocess.run(["bash", script_path, submit, workload_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output_lines = result.stdout.splitlines()
    for line in output_lines:
        if line.find("ID"):
            output_line = line
    workload_id = output_line.rsplit(maxsplit=1)[-1]
    output_filename = workload_id + "-swift-sample"
    print(f"Workload ID is: {workload_id}")
    while True:
        output_file_path = os.path.join(output_path, output_filename)  # Construct the absolute output file path
        if os.path.exists(output_file_path):
            # print(f"The file '{output_filename}' exists in the path '{output_path}'.")
            break
        time.sleep(1)
    result_file_path = os.path.join(result_path, workload_name)
    os.mkdir(result_file_path)
    output_csv_path = os.path.join(output_file_path, output_filename)
    output_csv_path += ".csv"
    result_csv_path = os.path.join(result_file_path, workload_name)
    result_csv_path += ".csv"
    shutil.copy2(output_csv_path,result_csv_path)

    os.remove(temp_output_file)
    os.remove(temp_output_file_xml)

    with open(result_csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        first_main_launching_time = None
        last_main_completed_time = None

        for row in reader:
            if row[0].find("main"):
                print(row)
                # if first_main_launching_time is None:
                #     first_main_launching_time = row[21]
                # last_main_completed_time = row[24]
    # print(f"start time was: {first_main_launching_time}")
    # print(f"completed time was: {last_main_completed_time}")
    print("--------------------------------------")
