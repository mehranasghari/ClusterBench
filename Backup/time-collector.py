#!/usr/bin/python3
import datetime
import os
import subprocess
import argparse
import shutil


def collect_times(directory_path):
    time_list = []

    # Iterate over the subdirectories in the specified directory
    for subdir in os.listdir(directory_path):
        subdir_path = os.path.join(directory_path, subdir)

        # Check if the subdirectory name matches the format "test-" followed by a number
        if os.path.isdir(subdir_path) and subdir.startswith("test-") and subdir[5:].isdigit():
            time_file_path = os.path.join(subdir_path, "time")

            # Read the content of the time file and append it to the time list
            if os.path.isfile(time_file_path):
                with open(time_file_path, "r") as time_file:
                    time_list.append(time_file.read().strip())

    return time_list

def save_times_to_file(time_list, output_file):
    with open(output_file, "w") as output:
        output.write("\n".join(time_list))

# Specify the directory path
directory_path = "/root/cosBench/ClusterBench/result"

# Collect times from the subdirectories
times = collect_times(directory_path)

# Save the times to the output file
output_file = "/root/scripts/input.txt"
save_times_to_file(times, output_file)

print("Times collected and saved to", output_file)
