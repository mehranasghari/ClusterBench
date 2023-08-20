import os
import subprocess
import argparse

def get_ring(host_file_path):

    # Read first line of hosts to execute ring files
    with open(host_file_path, 'r') as file:
        first_line = file.readline().strip()
        words = first_line.strip().split(',')

        user = words[0].strip()
        monster_host_ip = words[1].strip()
        monster_container_name = words[2].strip()

    ring_exec_command = f"ssh {user}@{monster_host_ip} docker exec {monster_container_name} swift-ring-builder /rings/account.builder > ./account-ring.txt"
    ring_exec_process = subprocess.run(ring_exec_command, shell=True)

if __name__ == "__main__":
    # Parse command-line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--hostfile", help="host file path")
    args = argParser.parse_args()

    if args.hostfile:
        # Call the function with the provided arguments
        result = get_ring(args.hostfile)
        print(result)
    else:
        print("Please provide a host file using the -f or --hostfile argument.")
