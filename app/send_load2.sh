#!/bin/bash

# send_load.sh - A script for sending load to a cluster

Usage(){
  cat << EOF
  
    send_load.sh [OPTIONS]

Options:
  -d, --default-file <file>   : Path to the default file. (Default: ./../conf/defaults.json)
  -b, --benchmark-file <file> : Path to the benchmark file. (Default: ./../conf/benchmark.cfg)
  -s, --script-file <file>    : Path to the script file. (Default: ./pre_test_script.sh)

Description:
  This script sends load to a cluster based on the provided benchmark and default files.
  Script-file executes before every test.

Example usage:
  send_load.sh -d /path/to/defaults.json -b /path/to/benchmark.cfg -s /path/to/script.sh
  send_load.sh -s /path/to/script.sh    (uses default benchmark and default files)

EOF
}


# Default input and default files
default_file="./../conf/defaults.json"
benchmark_file="./../conf/benchmark.cfg"
script_file="./pre_test_script.sh"

# Parse command line arguments
options=$(getopt -o d:b:s: --long default-file:,benchmark-file:,script-file: -n "$0" -- "$@")
eval set -- "$options"
while true; do
  case $1 in
    -d | --default-file) default_file=$2; shift 2 ;;
    -b | --benchmark-file) benchmark_file=$2; shift 2 ;;
    -s | --script-file) script_file=$2; shift 2 ;;
    --) shift; break ;;
    *) Usage; exit 1 ;;
  esac
done

# Call the main program
python3 main.py "${benchmark_file}" "${default_file}" "${script_file}"
