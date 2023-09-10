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
seconds_to_add = 3600  # For example, add 1 hour (3600 seconds)

# Add the specified number of seconds to both datetime objects
start_datetime += datetime.timedelta(seconds=seconds_to_add)
end_datetime += datetime.timedelta(seconds=seconds_to_add)

# Add the GMT+03:30 offset to both datetime objects
start_datetime_utc = start_datetime + datetime.timedelta(seconds=gmt_offset_seconds)
end_datetime_utc = end_datetime + datetime.timedelta(seconds=gmt_offset_seconds)

# Convert the UTC datetime objects back to strings
start_datetime_utc_str = start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
end_datetime_utc_str = end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")

# Print the UTC timestamps
print("Start Time (UTC):", start_datetime_utc_str)
print("End Time (UTC):", end_datetime_utc_str)

start_time , start_date = start_datetime_utc_str.strip().split(" ")
end_time , end_date = end_datetime_utc_str.strip().split(" ")
print ("start_time : " , start_time)
print("start_date : ", start_date)