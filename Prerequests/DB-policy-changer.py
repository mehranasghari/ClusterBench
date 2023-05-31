#!/usr/bin/python3
import os

print("\n\n\n\n")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-* ATTENTION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(" DO NOT USE influxDB after running this script for at least 2 HOURS ")
print(" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("\n\n\n\n")
Print (''' This code will change the retention polcy of the influxdb from what ever it set to shard duration 1H''')



# Receive the name of the container that influxDB is running in
container_name = input("Please enter your InfluxDB container name (default is 'influxdb2'): ")
if container_name == "":
    container_name = "influxdb2"

# Receive the name of the retention policy
rp_name = input("\nPlease enter your active retention policy name (default is 'autogen'): ")
if rp_name == "":
    rp_name = "autogen"

# Receive the name of the database
db_name = input ("\nPlease enter your database name (default is 'opentsdb'): ")
if db_name == "":
    db_name = "opentsdb"
print("\n")
print ("Selected contaoiner is : " , container_name,"selected retention policy : ", rp_name,"selected DB : " ,db_name)

# Modify the command and run it via docker exec
command = f"influx -execute 'alter retention policy {rp_name} on {db_name} shard duration 1h default'"
os.system(f"docker exec -it {container_name} {command}")

