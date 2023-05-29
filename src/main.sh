#!/bin/bash

# Default values
default_file=""
input_file=""

# Parse command line arguments
while getopts "d:i:p:" opt; do
  case $opt in
    d) default_file=$OPTARG ;;
    i) input_file=$OPTARG ;;
    p) prepare_file=$OPTARG ;;
    *) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done

# Check if required arguments are provided
if [[ -z $input_file ]]; then
  echo "Input file is required. Usage: script.sh -d default_file -i input_file" >&2
  exit 1
fi
if [[ -z $default_file ]]; then
  echo "Input file is required. Usage: script.sh -d default_file -i input_file" >&2
  exit 1
fi

python3 main.py "${input_file}" "${default_file}" "${prepare_file}"
