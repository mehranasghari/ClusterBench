#!/bin/bash

# Default values
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
