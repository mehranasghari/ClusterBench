#!/usr/bin/python3
import os

print()
print()
print()
print()
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(" DO NOT USE influxDB after ruuning this script for at least 2 HOUR ")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print()
print()
print()
print()

#name of the container that influxd is running in it.
container_name = "influxdb2"

# modify command and run it via docker exec
query = "influx -execute 'alter retention policy autogen on opentsdb shard duration 1h default'"

os.system(f'docker exec -it {container_name} {query}')

print()
print()
print()
print()
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(" DO NOT USE influxDB after ruuning this script for at least 2 HOUR ")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print()
print()
print()
print()
