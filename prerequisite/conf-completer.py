import os
import subprocess
import json

influxdb_container_name = input(f"Please enter your InfluxDB container name (Default : influxdb): ")
if influxdb_container_name == "":
    influxdb_container_name = "influxdb"

# Docker command
main_mount_command = f"docker inspect -f '{{range .Mounts}}{{if eq .Mode \"rw\"}}{{.Source}} {{.Destination}}{{end}}{{end}}' {influxdb_container_name}"
main_mount_process = subprocess.run(main_mount_command, shell=True)
