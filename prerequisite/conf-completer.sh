#!/bin/bash

read -p "Please enter your InfluxDB container name: " influxdb_container_name
if [ -z "$influxdb_container_name" ]; then
    influxdb_container_name="influxdb"
fi

# Capture the output of the docker inspect command into a variable
mount_output=$(docker inspect -f '{{range .Mounts}}{{if eq .Mode "rw"}}{{.Source}} {{.Destination}}{{end}}{{end}}' "$influxdb_container_name")

# Use read to split the output into two variables
read -r Main_influxdb_address_in_host Main_influxdb_in_container_address <<< "$mount_output"

# Read the existing JSON file
existing_json=$(cat ./test.json)

# Create a new JSON object with the new values
new_json=$(jq --arg sp "$source_path" --arg dp "$destination_path" \
             '. + {"new_key": {"Main_influxdb_address_in_host": $sp, "Main_influxdb_in_container_address": $dp}}' <<< "$existing_json")

# Write the modified JSON back to the file
echo "$new_json" > existing.json

echo "JSON file 'existing.json' updated with new values."
