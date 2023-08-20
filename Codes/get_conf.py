import os
import subprocess
import argparse

def get_conf(host_file_path):

    # Read first line of hosts to execute ring files
    with open(host_file_path, 'r') as file:
        lines = file.readlines().strip()
        for line in lines:
            words = line.strip().split(',')

            user = words[0].strip()
            monster_host_ip = words[1].strip()
            monster_container_name = words[2].strip()


if __name__ == "__main__":
    # Parse command-line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--hostfile", help="host file path")
    args = argParser.parse_args()

    if args.hostfile:
        # Call the function with the provided arguments
        result = get_conf(args.hostfile)
    else:
        print("Please provide a host file using the -f or --hostfile argument.")