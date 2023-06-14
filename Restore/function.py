# Specify the file path and name
file_path = './result.py'

# Open the file
with open(file_path, 'r') as file:
    # Read the first line
    first_line = file.readline().strip()
    
    # Evaluate the line as a Python expression
    data = eval(first_line)
    
    # Initialize variables for sum and count
    total_mean = 0
    count = 0
    
    # Iterate over the dictionaries and calculate the sum and count
    for item in data:
        mean = item['mean']
        total_mean += mean
        count += 1
    
    # Calculate the average
    if count > 0:
        average = total_mean / count
    else:
        average = 0
    
    # Print the result
    print("Sum of mean values:", total_mean)
    print("Count:", count)
    print("Average:", average)
