#!/usr/bin/env python3

import argparse
import sys
import getopt
import os
import subprocess

# Process given Test name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-C", "--Customized", default=False, help="if -C speecified main2 will be excuted, otherwise original main will be excuted")
args = argParser.parse_args()
mainswitch = args.Customized

def usage():
    print("""
    send_load.py [OPTIONS]

Options:
  -d, --default-file <file>   : Path to the default file. (Default: ./../conf/defaults.json)
  -b, --benchmark-file <file> : Path to the benchmark file. (Default: ./../conf/benchmark.cfg)
  -s, --script-file <file>    : Path to the script file. (Default: ./pre_test_script.sh)

Description:
  This script sends load to a cluster based on the provided benchmark and default files.
  Script-file is executed before every test.

Example usage:
  send_load.py -d /path/to/defaults.json -b /path/to/benchmark.cfg -s /path/to/script.sh
  send_load.py -s /path/to/script.sh    (uses default benchmark and default files)
""")


def main(argv):
    # Default input and default files
    default_file = "./../conf/Workload/defaults.json"
    benchmark_file = "./../conf/Workload/benchmark.cfg"
    script_file = "./pre_test_script.sh"

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(argv, "hd:b:s:", ["default-file=", "benchmark-file=", "script-file="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-d", "--default-file"):
            default_file = arg
        elif opt in ("-b", "--benchmark-file"):
            benchmark_file = arg
        elif opt in ("-s", "--script-file"):
            script_file = arg
    if mainswitch:
    # Call the main program 
    #print(f"Calling main program with benchmark_file: {benchmark_file}, default_file: {default_file}, script_file: {script_file}")
        run = f"python3 main2.py {benchmark_file} {default_file} {script_file} -p ./../cosbench-xml/workload-gen/all-xml"
        run_process = subprocess.run(run,shell=True)
    else :
        print ("Not developed yet ! :(")

if __name__ == "__main__":
    main(sys.argv[1:])