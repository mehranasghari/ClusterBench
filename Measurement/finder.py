import json
import os
import subprocess
import argparse

def finder(metric):
    matching_lines = []

    # Define addresses file path
    Influxdb_config_file_path = "./../conf/Software/InfluxdbConfig.json"
    exported_measurements_file_path = "./all-measurements.txt"

    # Check given metric with all metrics
    with_out_start_metric = metric[:-1]
    with open(exported_measurements_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if with_out_start_metric in line:
                matching_lines.append(line)

    return matching_lines

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--metric", help="Metric name which contains \"*\"")
    args = argParser.parse_args()
    metric = args.metric

    matching_lines = finder(metric)