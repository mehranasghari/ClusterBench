
import csv
import os

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

