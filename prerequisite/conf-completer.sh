#!/bin/bash

read -p "Please enter your InfluxDB container name: " influxdb_container_name
if [ -z "$influxdb_container_name" ]; then
    influxdb_container_name="influxdb"
fi

# Capture the output of the docker inspect command into a variable
mount_output=$(docker inspect -f '{{range .Mounts}}{{if eq .Mode "rw"}}{{.Source}} {{.Destination}}{{end}}{{end}}' "$influxdb_container_name")

# Use read to split the output into two variables
read -r source_path destination_path <<< "$mount_output"

# Print the captured output
echo "Source Path: $source_path"
echo "Destination Path: $destination_path"
