import csv

# Open the input file
with open('file.csv', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

# Extract the first 18 lines
first_18_lines = lines[:18]

# Calculate means for different ranges
ranges = [(30, 40), (41, 51), (52, 62), (63, 74), (75, 85)]
range_data = []
for start, end in ranges:
    numbers = [float(line.strip()) for line in lines[start - 1 : end]]
    range_data.append(numbers)

# Prepare the data for CSV
csv_data = []
for line in first_18_lines:
    # Split each line into columns
    columns = line.split()
    csv_data.append(columns)

# Transpose the range data
transposed_data = list(map(list, zip(*range_data)))

# Append the transposed range data as new columns
for i in range(len(csv_data)):
    csv_data[i].extend(transposed_data[i])

# Write the data to a CSV file
with open('output_file.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
