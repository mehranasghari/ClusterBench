import os
import subprocess
import argparse

# Define pathes
ring_file_excueter_file_path = "./ring_file_excuter.sh"
mover_file_path = "./mover.sh"

# Process given host file name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-h", "--hostfile", help="host file path")
args = argParser.parse_args()
host_file_path = args.hostfile

# Process given mc file name as an argument
argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--mchosts", help="host file path")
args = argParser.parse_args()
mc_host_file_path = args.mchosts

def get_ring(host_file_path, mc_host_file_path):
    ring_file_excueter_file_path = "./ring_file_excuter.sh"
    mover_file_path = "./mover.sh"

    # Read first line of hosts to execute ring files
    with open(host_file_path, 'r') as file:
        first_line = file.readline().strip()
        words = first_line.strip().split(',')

        monster_host_name = words[0].strip()
        monster_host_ip = words[1].strip()
        monster_container_name = words[2].strip()

    # Read first line of mc hosts to be able to move ring files
    with open(mc_host_file_path, 'r') as file:
        first_line = file.readline().strip()
        words = first_line.strip().split()

        mc_host_name = words[0].strip()
        mc_host_ip = words[1].strip()

    # delete file if exists
    del_command = "rm -rf ./ring_file_excuter.sh"
    del_process = subprocess.run(del_command, shell=True)
    del_exit_code = del_process.returncode

    # Generate and complete ring-file-excuter.sh
    with open(ring_file_excueter_file_path , 'a') as file:
        file.write("swift-ring-builder /rings/account.builder > /account.txt")
        file.write(f"\nswift-ring-builder /rings/object.builder > /object.txt")
        file.write(f"\nswift-ring-builder /rings/container.builder > /container.txt")

    # Check if file generated successfully or not
    with open(ring_file_excueter_file_path, 'r') as file:
        content = file.read()

    if content.strip():
        print("\033[92mRing File Excuter Generated Successfully\033[0m")
    else:
        print("\033[91mRing File Excuter Generating Failed.\033[0m")

    # Scp file to monster vm
    trasnfer_command = f"scp ./ring_file_excuter.sh {monster_host_name}:/ > /dev/null 2>&1"
    trasnfer_process = subprocess.run(trasnfer_command, shell=True)
    trasnfer_exit_code = trasnfer_process.returncode
    if trasnfer_exit_code == 0 :
        print("\033[92mring-file-excuter moved Successfully\033[0m")
    else:
        print("try to scp via ip, scp with name failed")
        trasnfer_command = f"scp ./ring_file_excuter.sh {monster_host_ip}:/ > /dev/null 2>&1"
        trasnfer_process = subprocess.run(trasnfer_command, shell=True)
        trasnfer_exit_code_ip = trasnfer_process.returncode
        if trasnfer_exit_code_ip == 0:
            print("\033[92mring-file-excuter moved Successfully\033[0m")
        else:
            print("scp failed")

    # Delete mover if exists
    mover_rm_command = f"rm -rf {mover_file_path}"
    mover_rm_process = subprocess.run(mover_rm_command, shell=True)
    mover_rm_exit_code = mover_rm_process.returncode
    if mover_rm_exit_code == 0:
        print("\033[92mmover deleted Successfully\033[0m")

    # Generate mover
    with open(mover_file_path, 'w') as file :
        file.write(f"docker cp {monster_container_name}:/account.txt /account.txt")
        file.write(f"docker cp {monster_container_name}:/object.txt /object.txt")
        file.write(f"docker cp {monster_container_name}:/container.txt /container.txt")
        file.write(f"scp /account.txt /object.txt /container.txt {mc_host_name}:/")

    # Transfer mover.sh to monster container
    trasnfer2_command = f"scp ./mover.sh {monster_host_name}:/ > /dev/null 2>&1"
    trasnfer2_process = subprocess.run(trasnfer2_command, shell=True)
    trasnfer2_exit_code = trasnfer2_process.returncode
    if trasnfer2_exit_code == 0 :
        print("\033[92mmover moved Successfully\033[0m")

    # cp file to monster container
    docker_cp_command = f"ssh {monster_host_name} docker cp /ring_file_excuter.sh {monster_container_name}:/ > /dev/null 2>&1"
    docker_cp_process = subprocess.run(docker_cp_command, shell=True)
    docker_cp_exit_code = docker_cp_process.returncode
    if docker_cp_exit_code == 0:
        print("\033[92mring-exuter moved to container successfully\033[0m")

    # excute the script
    execute_command = f"ssh {monster_host_name} docker exec -t storage \"bash /ring_file_excuter.sh\""
    execute_process = subprocess.run(execute_command, shell=True)
    execute_exit_code = execute_process.returncode
    if execute_exit_code == 0:
        print("\033[92mring-file executed Successfully\033[0m")

    # Run mover.sh
    execute2_command = f"ssh {monster_host_name} \"bash /mover.sh\""
    execute2_process = subprocess.run(execute_command, shell=True)
    execute2_exit_code = execute2_process.returncode
    if execute2_exit_code == 1:
        print("\033[92mmover runned Successfully\033[0m")

    # Mv to config file 
    mv_command = f"mv /*.txt ."
    mv_process = subprocess.run(mv_command, shell=True)
    mv_exit_code = mv_process.returncode
    if mv_exit_code == 1 :
        print("mv error")


if __name__ == "__main__":
    # Parse command-line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-h", "--hostfile", help="host file path")
    argParser.add_argument("-m", "--mchosts", help="mc host file path")
    args = argParser.parse_args()

    # Call the function with the provided arguments
    result = get_ring(args.hostfile, args.mchosts)
    print(result)