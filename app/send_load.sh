#!/bin/bash

# send_load.sh - A script for sending load to a cluster

# Usage:
#   send_load.sh [OPTIONS]

# Options:
#   -d, --default-file <file>   : Path to the default file. (Default: ./../conf/defaults.json)
#   -i, --input-file <file>     : Path to the input file. (Default: ./../conf/benchmark.cfg)
#   -s, --script-file <file>    : Path to the script file.

# Description:
#   This script sends load to a cluster based on the provided input and default files.

# Example usage:
#   send_load.sh -d /path/to/defaults.json -i /path/to/benchmark.cfg -s /path/to/script.sh
#   send_load.sh -s /path/to/script.sh    (uses default input and default files)

# Default input and default files
default_file="./../conf/defaults.json"
input_file="./../conf/benchmark.cfg"

# Parse command line arguments
while getopts "d:i:s:" opt; do
  case $opt in
    d) default_file=$OPTARG ;;
    i) input_file=$OPTARG ;;
    s) script_file=$OPTARG ;;
    *) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done

# Call the main program
python3 main.py "${input_file}" "${default_file}" "${script_file}"
