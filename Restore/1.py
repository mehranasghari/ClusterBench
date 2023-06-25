import os
import shutil
import datetime
import os
import subprocess
import argparse
from influxdb import InfluxDBClient
import subprocess
import calendar
import sys
import os

def get_first_subdirectory(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if dirnames:  # Check if there are any subdirectories
            first_subdirectory = dirnames[0]
            print("First subdirectory:", first_subdirectory)
#            return first_subdirectory

# Provide the root directory path
root_directory_path = "/mnt/sdb/influx-test/influxdb-data/tarred-files"

# Call the function to get the first subdirectory
first_subdirectory = get_first_subdirectory(root_directory_path)

# Print the first subdirectory
#print("First subdirectory:", first_subdirectory)

