import datetime

# Define the GMT+03:30 offset in seconds
gmt_offset_seconds = 3 * 3600 + 30 * 60

# Read the line from the file (assuming it's stored in a variable called 'line')
line = "2023-09-05 23:45:15,2023-09-06 00:55:20"

# Split the line by ","
start_datetime_str, end_datetime_str = line.strip().split(",")

# Convert start and end datetime strings to datetime objects
start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")

# Define the number of seconds to add
seconds_to_add = 300  # For example, add 1 hour (3600 seconds)

# Add the GMT+03:30 offset to both datetime objects
start_datetime_utc = start_datetime - datetime.timedelta(seconds=gmt_offset_seconds)
end_datetime_utc = end_datetime - datetime.timedelta(seconds=gmt_offset_seconds)

dir_start_datetime_utc = start_datetime - datetime.timedelta(seconds=gmt_offset_seconds)
dir_end_datetime_utc = end_datetime - datetime.timedelta(seconds=gmt_offset_seconds)

# Add the specified number of seconds to both datetime objects
start_datetime_utc -= datetime.timedelta(seconds=seconds_to_add)
end_datetime_utc += datetime.timedelta(seconds=seconds_to_add)

# Convert the UTC datetime objects back to strings
start_datetime_utc_str = start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
end_datetime_utc_str = end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")

# creating backup time format
backup_start_date , backup_start_time = start_datetime_utc_str.split(" ")
start_time_backup = backup_start_date+"T"+backup_start_time+"Z"
backup_end_date , backup_end_time = end_datetime_utc_str.split(" ")
end_time_backup = backup_end_date+"T"+backup_end_time+"Z"

print("start_time_backup : ", start_time_backup)
print("end_time_backup : ", end_time_backup)

# dir name creation
dir_start_datetime_utc_str = dir_start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
dir_end_datetime_utc_str = dir_end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
dir_start_date , dir_start_time = dir_start_datetime_utc_str.split(" ")
dir_start_date = dir_start_date[2:].replace("-","")
dir_start_time = dir_start_time.replace(":","")
dir_end_date , dir_end_time = dir_end_datetime_utc_str.split(" ")
dir_end_date = dir_end_date[2:].replace("-","")
dir_end_time = dir_end_time.replace(":","")
backup_dir_name = dir_start_date+"T"+dir_start_time+"_"+dir_end_date+"T"+dir_end_time
print("backup_dir_name : " , backup_dir_name)
print("dir_start_date :" , dir_start_date)
print("dir_start_time : ", dir_start_time)
print("dir_end_date : ", dir_end_date)
print("dir_end_time : ", dir_end_time)
# Print the UTC timestamps
#print("Start Time (UTC):", start_datetime_utc_str)
#print("End Time (UTC):", end_datetime_utc_str)
