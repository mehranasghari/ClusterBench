# this is a sample of conf completer
import os
import subprocess
import json

# Search and find main influxdb mount points
influxdb_container_name = input(f"Please enter your InfluxDB container name (Default :storage ): ")
if influxdb_container_name == "":
    influxdb_container_name = storage
main_mount_command = f"docker inspect -f \'{{range .Mounts}}{{if eq .Mode \"rw\"}}{{.Source}} {{.Destination}}{{end}}{{end}}\' "
main_mount_process = subprocess.run(main_mount_command, shell=True)
print("\n",main_mount_command)