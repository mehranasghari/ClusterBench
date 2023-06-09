from influxdb import InfluxDBClient
import os
import datetime
import subprocess
import argparse
import calendar
import json
import pytz
import csv

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
            output_file = f'{directorypath}/{dir_backup}/csv/{host}_first_output.txt'

            with open(output_file, 'w') as file:
                for series in result:
                    for point in series:
                        file.write(str(point) + '\n')

            print(f"CSV for {host} saved to {output_file}")
        
        # Process the csv files
        # Specify the directory path containing the result.txt files
        directory_path = f'{directorypath}/{dir_backup}/csv'

        # Specify the output file path
        output_file_path = '{directorypath}/{dir_backup}/csv'

        # Create a list to store the input file paths
        input_file_paths = []

        # Iterate over each file in the directory
        for file_name in os.listdir(directory_path):
          if file_name.endswith('.txt'):
            file_path = os.path.join(directory_path, file_name)
            input_file_paths.append(file_path)

        # Open the output file
        with open(output_file_path, 'w', newline='') as output_file:
        # Create a CSV writer
          writer = csv.writer(output_file)

        # Iterate over each input file
        for input_file_path in input_file_paths:
        # Open the input file
          with open(input_file_path, 'r') as input_file:
            # Iterate over each line in the input file
            for line in input_file:
                # Strip any leading/trailing whitespace
                line = line.strip()

                # Evaluate the line as a Python expression
                data = eval(line)

                # Calculate the sum and count
                total_mean = sum(item['mean'] for item in data)
                count = len(data)

                # Calculate the average
                if count > 0:
                    average = total_mean / count
                else:
                    average = 0

                # Write the mean value to the CSV file
                writer.writerow([average])

        # Print a message to indicate the CSV file has been created
        #print(f"Results saved to {output_file_path}")

        # ------------------- PHASE 2 ------------------

        def extract_lines_to_csv(input_dir, output_csv_path, num_lines=18):
            csv_file_paths = []

          # Discover all .csv files in the input directory
            for file_name in os.listdir(input_dir):
              if file_name.endswith(".csv"):
                csv_file_paths.append(os.path.join(input_dir, file_name))

            with open(output_csv_path, 'w', newline='') as output_csv:
              writer = csv.writer(output_csv)

            for csv_file_path in csv_file_paths:
                with open(csv_file_path, 'r') as csv_file:
                  reader = csv.reader(csv_file)
                  lines = [next(reader) for _ in range(num_lines)]  # Read the specified number of lines from the CSV file
                
                  # Write the first 18 lines to the CSV file
                  writer.writerows(lines)

                  # Calculate the mean of lines 19 to 29 and Write the mean value to the CSV file
                  values = [float(line[0]) for line in reader]  # Read the remaining lines
                  mean = sum(values[0:10]) / len(values[0:10])
                  print("values 19:29 are :" , values[0:10])
                  print(" len values[19:29] is : ", len(values[0:10]))
                  print("mean is :" , mean)
                  writer.writerow([mean])

                  # Calculate the mean of lines 30 to 39 Write the mean value to the CSV file
                  mean = sum(values[10:20]) / len(values[10:20])
                  # print("values 30:39 are :" , values[10:20])
                  # print(" len values[30:39] is : ", len(values[10:20]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])

                  # Calculate the mean of lines 40 to 49 # Write the mean value to the CSV file
                  mean = sum(values[20:30]) / len(values[20:30])
                  # print("values 1 are :" , values[20:30])
                  # print(" len values[40:49] is : ", len(values[20:30]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])
                  
                  # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                  mean = sum(values[30:40]) / len(values[30:40])
                  # print("values 2 are :" , values[30:40])
                  # print(" len values[30:39] is : ", len(values[30:40]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])
                                  
                  # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                  mean = sum(values[40:50]) / len(values[40:50])
                  # print("values 3 are :" , values[40:50])
                  # print(" len values[30:39] is : ", len(values[40:50]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])

                  # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                  # mean = sum(values[50:60]) / len(values[50:60])
                  # print("values 4 are :" , values[50:60])
                  # print(" len values[30:39] is : ", len(values[50:60]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])

                  # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                  mean = sum(values[60:67]) / len(values[60:67])
                  # print("values 5are :" , values[60:67])
                  # print(" len values[30:39] is : ", len(values[60:67]))
                  # print("mean is :" , mean)
                  writer.writerow([mean])


                  input_dir = f"{directorypath}/{dir_backup}/csv"
                  output_csv_path = f"{directorypath}/{dir_backup}/csv"
                  extract_lines_to_csv(input_dir, output_csv_path, num_lines=18)