import subprocess
import os

# Drop database
container_name = 'influxdb2'
database_name = 'opentsdb'
command = f"influx -execute 'drop database {database_name}'"
os.system(f"docker exec -it {container_name} {command}")
print(" -------------------- Drop database Done!  --------------------")

def extract_tar_gz(file_path, extraction_path):
    try:
        # Create the extraction directory if it doesn't exist
        os.makedirs(extraction_path, exist_ok=True)

        # Extract the .tar.gz file to the desired path
        subprocess.run(['tar', '-xf', file_path, '-C', extraction_path], check=True)

        print('\033[92mExtraction successful!\033[0m')

    except subprocess.CalledProcessError:
        print('\033[91mExtraction failed!\033[0m')


# Example usage
file_name = input("Enter the file name: ")
file_path = f"/root/monster/hayoola-mc/influxdb-data/test-backup/{file_name}"
extraction_path = '/mnt/sdb/influx-test/influxdb-data/untarred-files/'

extract_tar_gz(file_path, extraction_path)


print("------------------ Start Restore  ------------------")
command2 = "influxd restore -portable /var/lib/influxdb/untarred-files/"
os.system(f"docker exec -it {container_name} {command2}")
print("------------------ END Restore  ------------------")


print("------------ Start remove files ------------")
command3 = "rm -rf /mnt/sdb/influx-test/influxdb-data/untarred-files/*"
os.system(f"{command3}")
print("------------ END remove files --------------------")
