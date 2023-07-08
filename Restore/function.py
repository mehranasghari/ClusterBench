import csv
import os

# Specify the directory path containing the result.txt files
directory_path = './'

# Specify the output file path
output_file_path = './first-generated.csv'

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

                # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                #values = [float(line[0]) for line in reader]  # Read the remaining lines
                mean = sum(values[11:21]) / len(values[11:21])
                print("values 30:39 are :" , values[11:21])
                print(" len values[30:39] is : ", len(values[11:21]))
                print("mean is :" , mean)
                writer.writerow([mean])

                # Calculate the mean of lines 40 to 49 # Write the mean value to the CSV file
                #values = [float(line[0]) for line in reader]  # Read the remaining lines
                mean = sum(values[21:31]) / len(values[21:31])
                print("values 40:49 are :" , values[21:31])
                print(" len values[40:49] is : ", len(values[21:31]))
                print("mean is :" , mean)
                writer.writerow([mean])
                
                # Calculate the mean of lines 30 to 39 # Write the mean value to the CSV file
                #values = [float(line[0]) for line in reader]  # Read the remaining lines
                mean = sum(values[31:41]) / len(values[31:41])
                print("values 40:49 are :" , values[31:41])
                print(" len values[30:39] is : ", len(values[31:41]))
                print("mean is :" , mean)
                writer.writerow([mean])

input_dir = "./"
output_csv_path = "./output.csv"

extract_lines_to_csv(input_dir, output_csv_path, num_lines=18)
