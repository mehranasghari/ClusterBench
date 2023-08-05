import argparse
import os 
import subprocess 

def main():
    parser = argparse.ArgumentParser()
    
    # Define the arguments with default values
    parser.add_argument('-d', '--arg_b', default="./../conf/defaults.json", help="Path to the default file.")
    parser.add_argument('-b', '--arg_d', default="./../conf/benchmark.cfg", help="Path to the benchmark file.")
    parser.add_argument('-s', '--arg_s', default="./pre_test_script.sh", help="Path to the script file.")

    args = parser.parse_args()

    # Access the argument values
    benchmark_file = args.arg_b
    default_file = args.arg_d
    script_file = args.arg_s

    # Use the argument values in your application logic
    print(f'Argument B: {benchmark_file}')
    print(f'Argument D: {default_file}')
    print(f'Argument S: {script_file}')
    
    # Run main.py
    call_command = f" python3 main.py {benchmark_file} {default_file} {script_file}"
    call_process = subprocess.run(call_command, shell=True)

if __name__ == '__main__':
    main()