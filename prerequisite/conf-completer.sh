#!/bin/bash

read -p "Please enter your InfluxDB container name: " influxdb_container_name
if [ -z "$influxdb_container_name" ]; then
    influxdb_container_name="influxdb"
fi

docker inspect -f '{{range .Mounts}}{{if eq .Mode "rw"}}{{.Source}} {{.Destination}}{{end}}{{end}}' $influxdb_container_name