import datetime

def convert_to_timestamp(input_time):
    try:
        # Check if the input is a timestamp
        timestamp = int(input_time)
        
        # Convert timestamp to datetime object
        time = datetime.datetime.fromtimestamp(timestamp / 1000)  # Divide by 1000 to convert milliseconds to seconds
        
        # Format the datetime object as a string
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time
    except ValueError:
        try:
            # Convert normal time to datetime object
            time = datetime.datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
            
            # Convert datetime object to timestamp in milliseconds
            timestamp = int(time.timestamp() * 1000)
            return timestamp
        except ValueError:
            return 'Invalid input'

# Read input from the user
input_time = input('Enter a timestamp or a normal time (YYYY-MM-DD HH:MM:SS): ')

# Convert the input to timestamp or normal time
converted_time = convert_to_timestamp(input_time)

# Print the converted time
print(converted_time)
