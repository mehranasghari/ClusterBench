import sys
import subprocess
import generate_xml
import os
import time

script_path = './../../cli.sh'
output_path = './../../archive/'
arg1 = 'submit'

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
    print(f"Workload: {workload_name} is running")
    arg2 = temp_output_file_xml
    result = subprocess.run(["bash", script_path, arg1, arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output_lines = result.stdout.splitlines()
    for line in output_lines:
        if line.find("ID"):
            output_line = line
    workload_id = output_line.rsplit(maxsplit=1)[-1]
    output_filename = workload_id + "-swift-sample"
    while True:
        output_file_path = os.path.join(output_path, output_filename)  # Construct the absolute file path
        if os.path.exists(output_file_path):
            print(f"The file '{output_filename}' exists in the path '{output_path}'.")
            break
        time.sleep(1)
    os.remove(temp_output_file)
    os.remove(temp_output_file_xml)
    print("--------------------------------------")
