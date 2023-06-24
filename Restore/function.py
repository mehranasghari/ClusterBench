
import csv

# Specify the file paths
input_file_path = './result.txt'
output_file_path = './file.csv'
hosts = './../Hosts/hosts.txt'

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    # Create a CSV writer
    writer = csv.writer(output_file)

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
print(f"Results saved to {output_file_path}")
# Specify the file path and name
file_path = './result.txt'

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

import csv

def extract_lines_to_csv(txt_file_path, csv_file_path, num_lines=18):
    with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
        lines = txt_file.readlines()[:num_lines]  # Read the specified number of lines from the text file

        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow([line.strip()])
txt_file_path = "path/to/your/file.txt"
csv_file_path = "path/to/save/your/output.csv"

extract_lines_to_csv(txt_file_path, csv_file_path, num_lines=18)
