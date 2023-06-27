from influxdb import InfluxDBClient
import os
import datetime
import subprocess
import argparse
import calendar
import json
import pytz

# Specify address to config files
address_file_path = "./../conf/address.json"
hosts_file_path = "./../Hosts/hosts-test.txt"

# Load the JSON data from the file and define adresses as a variable 
with open(address_file_path, 'r') as file:
    json_data = json.load(file)
Secondry_influxdb_in_container_address = json_data['Secondry_influxdb_in_container_address']
Secondary_influxdb_container_name = json_data['Secondary_influxdb_container_name']
Secondary_influxdb_DB_name = json_data['Secondary_influxdb_DB_name']
Secondary_influxdb_address_in_host = json_data['Secondary_influxdb_address_in_host']

# Process given directory name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--directorypath", help="Directory path (Directory which contain backup directories)")
args = argParser.parse_args()
directorypath = args.directorypath

# Check that fiven address is not empty and check the correct path 
#if directorypath == "":
 #   directorypath = Secondary_influxdb_address_in_host
#elif directorypath != f"{Secondary_influxdb_address_in_host}/*":
  # print(f"\033[91mGiven Path is not in mountpoint of Secondary influxdb\033[0")
  # directorypath = input("\nEnter address in Secondary influxdb which contain backup directories : ")
backup_dir_list = os.listdir(directorypath)

for dir_backup in backup_dir_list:
    
    # Drop DB
    drop_command = f"docker exec -it {Secondary_influxdb_container_name} influx -execute 'drop database {Secondary_influxdb_DB_name}'"
    drop_process = subprocess.run(drop_command, shell=True)
    exit_code = drop_process.returncode
    if exit_code == 0:
      print(f"\033[92mDatabase {Secondary_influxdb_DB_name} successfully.\033[0m")
      print()
    else:
      print(f"\033[91mDropping {Secondary_influxdb_DB_name} failed.\033[0m")
      print()
      break

    # Extract the backup.tar.gz
    extract_command = f"tar -xf {directorypath}/{dir_backup}/*.tar.gz -C {directorypath}/{dir_backup}/backup/"
    extract_process = subprocess.run(extract_command, shell=True)
    exit_code = extract_process.returncode
    if exit_code == 0:
      print("\033[92mBackup extracted successfully.\033[0m")
      print()
    else:
      print("\033[91mExtraction failed.\033[0m")
      print()
      break

    # Restore on influxdb
    restore_command = f"docker exec -it {Secondary_influxdb_container_name} influxd restore -portable {Secondry_influxdb_in_container_address}/{dir_backup}/backup/ >/dev/null"
    restore_process = subprocess.run(restore_command, shell=True)
    exit_code = restore_process.returncode
    if exit_code == 0:
     print("\033[92mFiles restored successfully.\033[0m")
     print()
    else:
     print("\033[91mRestore failed.\033[0m")
     print()  
     break

    # Create csv dir 
    os.makedirs(f"mkdir {directorypath}/{dir_backup}/csv", exist_ok=True)

    # Read time of backup from each directory
    from datetime import datetime
    time_file_path = f"{Secondary_influxdb_address_in_host}/{dir_backup}/info/time"
    with open(time_file_path, "r") as file:
        time_str = file.read().strip()
        time_values = time_str.split(",")
        start_time, end_time = time_values[0], time_values[1]
        start_time_query = calendar.timegm(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
        end_time_query = calendar.timegm(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
        
        # Set up the InfluxDB connection
        group_by = 'time(10s)'
        host = 'localhost'
        port = 8086
        database = f'{Secondary_influxdb_DB_name}'
        client = InfluxDBClient(host=host, port=port, database=database)

    # CSV creation function
    with open(hosts_file_path, "r") as file:
        hosts = file.readlines()     # Read the hosts from the file
        hosts = [host.strip() for host in hosts] # Remove any whitespace characters from the end of each line
    
        # Iterate over each host and execute code
        for host in hosts:

            query = 'SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.account_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.account_server.head.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.head.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.get.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.delete.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.delete.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.user" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.system" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.iowait" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.idle" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.net.received" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.system.net.sent" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.cached" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.buffers" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.free" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdb.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdc.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdd.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sde.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdf.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdg.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdh.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdi.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdj.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdk.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdl.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdb.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdc.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdd.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sde.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdf.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdg.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdh.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdi.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdj.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdk.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdl.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdb.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdc.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdd.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sde.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdf.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdg.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdh.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdi.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdj.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdk.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdl.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdb.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdc.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdd.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sde.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdf.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdg.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdh.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdi.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdj.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdk.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdl.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sda.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdb.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdc.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdd.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sde.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdf.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdg.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdh.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdi.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdj.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdk.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdl.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdb.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdc.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdd.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sde.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdf.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdg.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdh.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdi.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdj.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdk.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdl.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null)'

            # Run the query by variables
            query = query.format(group_by=group_by,host=host,start_time_query=start_time_query,end_time_query=end_time_query)
            result = client.query(query)
            
            # Save the query result to a file and clear the query result.tx with echonig "" to it.
            output_file = f'{directorypath}/{dir_backup}/csv/{host}_first_output.csv'

            with open(output_file, 'w') as file:
                for series in result:
                    for point in series:
                        file.write(str(point) + '\n')

            print(f"CSV for {host} saved to {output_file}")
        
        # Process the csv files
        