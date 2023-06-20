import datetime
import os
import subprocess
import argparse
from influxdb import InfluxDBClient
import subprocess
import calendar
import sys

print ("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START OF BACKUP *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--testname", help="Test Name (Directory in Result/)")
args = argParser.parse_args()
testDirectory = args.testname
global testDirectory2
testDirectory2 = args.testname

def read_values_from_file(file_path):
    values = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            values.extend(line.strip().split(","))
    return values

def process_input_file(file_path_input):
    # set config time in seconds manually
    x = 600
    y = 600

    with open(file_path_input, "r") as f:
        lines = f.readlines()
        for line in lines:

            global start_date
            global start_time
            global end_date
            global end_time

            start_datetime, end_datetime = line.strip().split(",")
            start_date, start_time = start_datetime.split(" ")
            end_date, end_time = end_datetime.split(" ")

            # Convert to datetime objects
            start_datetime = datetime.datetime.strptime(start_date + " " + start_time, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(end_date + " " + end_time, "%Y-%m-%d %H:%M:%S")

            # Convert to standard format (time only)
            start_time_standard = start_datetime.strftime("%H:%M:%S")
            end_time_standard = end_datetime.strftime("%H:%M:%S")

            # Remove all ":" for backup file name
            final_time_start_backup = start_time_standard.replace(":", "")
            final_time_end_backup = end_time_standard.replace(":", "")

            final_time_end = (end_datetime + datetime.timedelta(seconds=y)).strftime("%H:%M:%S")
            final_time_start = (start_datetime - datetime.timedelta(seconds=x)).strftime("%H:%M:%S")

            # Remove all ":" for directory name
            final_time_start_dir = final_time_start.replace(":", "")
            final_time_end_dir = final_time_end.replace(":", "")

            # Remove all "-" for directory name
            start_date_dir = start_date.replace("-", "")
            start_date_dir = start_date_dir[2:]
            end_date_dir = end_date.replace("-", "")
            end_date_dir = end_date_dir[2:]
            global backup_dir
            backup_dir = start_date_dir + "T" + final_time_start_backup + "_" + end_date_dir + "T" +final_time_end_backup
            backup_path2 = "/var/lib/influxdb/test-backup/" + backup_dir
            backup_path = f"/var/lib/influxdb/test-backup/{backup_dir}" + backup_dir
            os.makedirs(backup_path, exist_ok=True)
            start_time_backup = start_date + "T" + final_time_start + "Z"
            end_time_backup = end_date + "T" + final_time_end + "Z"

            # Perform backup using influxd backup command
            backup_command = f"docker exec -it influxdb influxd backup -portable -start {start_time_backup} -end {end_time_backup} {backup_path2}/backup >/dev/null "
            backup_process = subprocess.run(backup_command, shell=True)
            exit_code = backup_process.returncode
            if exit_code == 0:
                print("\033[92mBackup successful.\033[0m")
            else:
                print("\033[91mBackup failed.\033[0m")
                sys.exit(1)
            print()
            #cp and mv commands
            os.makedirs(f"/root/monster/hayoola-mc/influxdb-data/test-backup/{backup_dir}/info", exist_ok=True)
            cp_command = f"cp -r ./../result/{testDirectory}/* /root/monster/hayoola-mc/influxdb-data/test-backup/{backup_dir}/info/"
            cp_process = subprocess.run(cp_command, shell=True)

	        #MV BACKUP.TAR.GZ TO influxdb2
            mv_command = f"mv /root/monster/hayoola-mc/influxdb-data/test-backup/*  /mnt/sdb/influx-test/influxdb-data/tarred-files/"
            mv_process = subprocess.run(mv_command, shell=True)
            # Delete backup directory
            delete_command = f"docker exec -it influxdb rm -rf {backup_path}"
            delete_process = subprocess.run(delete_command, shell=True)
            delete_check = delete_process.returncode
            if delete_process.returncode == 0:
                print()
                print("\033[92mDeleting Directory Completed successfully.\033[0m")
            else:
                print()
                print("\033[91mDeleting Directory failed.\033[0m")
                sys.exit(1)

input_file = "./../result/"+testDirectory+"/time"
process_input_file(input_file)
print ("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END OF BACKUP *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print ("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START RESTORE *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

#info
container_name = 'influxdb2'
database_name = 'opentsdb'

# Drop database
# -------------------- START Drop database --------------------
command = f"influx -execute 'drop database {database_name}'"
os.system(f"docker exec -it {container_name} {command}")
# --------------------  END Drop database --------------------


#------------------ Start Restore  ------------------
command2 = f"influxd restore -portable /var/lib/influxdb/tarred-files/{backup_dir}/backup"
exit_code = os.system(f"docker exec -it {container_name} {command2} >/dev/null ")

if exit_code == 0:
    print()
    print("\033[92mRestore Done successfully.\033[0m")  # Print message in green
else:
    print("\033[91mRestore failed.\033[0m")  # Print message in red
    sys.exit(1)
# ------------------ END Restore  ------------------

print ("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END RESTORE *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print ("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START EXPORT CSV FILE *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


from datetime import datetime
hosts_file_path = "./../Hosts/hosts.txt"

# Set up the InfluxDB connection
host = 'localhost'
port = 8086
database = 'opentsdb'
client = InfluxDBClient(host=host, port=port, database=database)

# Set time to run query
start_time = start_date+" "+start_time
end_time = end_date+" "+end_time


# Set variables
group_by = 'time(10s)'
start_time_query = calendar.timegm(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
end_time_query = calendar.timegm(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.now().astimezone().tzinfo).timetuple()) * 1000
csv_address = f'/mnt/sdb/influx-test/influxdb-data/tarred-files/{backup_dir}/csv'
image_address = f'/mnt/sdb/influx-test/influxdb-data/tarred-files/{backup_dir}/images'
os.makedirs(csv_address, exist_ok=True)
os.makedirs(image_address, exist_ok=True)

# Read the hosts from the file
with open(hosts_file_path, "r") as file:
    hosts = file.readlines()

# Remove any whitespace characters from the end of each line
hosts = [host.strip() for host in hosts]

# Iterate over each host and execute code
for host in hosts:
    
    # Replace GROUP BY clause in the query with the variable
    query = 'SELECT mean("value") *-1 FROM "netdata.disk.sdb.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdc.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdd.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sde.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdf.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdb.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdc.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdd.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sde.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdf.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdg.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdh.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdi.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdj.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdk.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.disk.sdl.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdg.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdh.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdi.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdj.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdk.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk.sdl.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sda.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdb.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdc.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdd.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sde.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdf.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdg.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdh.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdi.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdj.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdk.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_util.sdl.utilization" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdb.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdc.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdd.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sde.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdf.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdg.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdb.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdc.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdd.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sde.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdf.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdg.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdh.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdi.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdj.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdk.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_ops.sdl.reads" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdh.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdi.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdj.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdk.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *(-1) FROM "netdata.disk_ops.sdl.writes" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.account_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.put.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.account_server.head.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.head.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.get.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.object_server.delete.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.statsd_timer_swift.container_server.delete.timing.events" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.user" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.system" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.iowait" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.cpu.idle" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.net.received" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") *-1 FROM "netdata.system.net.sent" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.cached" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.buffers" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.system.ram.free" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdb.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdc.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdd.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sde.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdf.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdg.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdh.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdi.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdj.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdk.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);SELECT mean("value") FROM "netdata.disk_inodes._srv_node_sdl.used" WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null)'


    query = query.format(group_by=group_by,host=host,start_time_query=start_time_query,end_time_query=end_time_query)
    result = client.query(query)

    # Save the query result to a file and clear the query result.tx with echonig "" to it.
    output_file = f'{csv_address}/{host}_{testDirectory2}.txt'

    with open(output_file, 'w') as file:
       for series in result:
           for point in series:
               file.write(str(point) + '\n')

    print(f"CSV for {host} saved to {output_file}")

print ("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END EXPORT CSV FILE *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
