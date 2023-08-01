import argparse
import os 
import subprocess 

def main(benchmark_file, default_file, script_file):
    # Your main logic here
    print(f"Benchmark File: {benchmark_file}")
    print(f"Default File: {default_file}")
    print(f"Script File: {script_file}")

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="A script for sending load to a cluster")

    # Add the command-line options
    parser.add_argument("-d", "--default-file", dest="default_file", default="./../conf/defaults.json", help="Path to the default file.")
    parser.add_argument("-b", "--benchmark-file", dest="benchmark_file", default="./../conf/benchmark.cfg", help="Path to the benchmark file.")
    parser.add_argument("-s", "--script-file", dest="script_file", default="./pre_test_script.sh", help="Path to the script file.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main program with the provided arguments
    main(args.benchmark_file, args.default_file, args.script_file)

# call main.py
call_command = f" python3 main.py {args.benchmark_file} {args.default_file} {args.script_file}"
call_process = subprocess.run(call_command, shell=True)
