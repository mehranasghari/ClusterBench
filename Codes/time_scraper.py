import os
import argparse

# Create an argument parser
argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--path", help="path to test dirs")
args = argParser.parse_args()
path = args.path

# Pathes
times_file_path = os.path.join(path, "time.txt")

# Check if the path is provided
if not path:
    print("Please provide a path using the -p or --path argument.")
else:
    # Check if the provided path exists
    if os.path.exists(path):
        # Function to list directories
        def time_scraper(path):
            dirs = os.listdir(path)
            for dir in dirs:
                time_file_path = os.path.join(path, dir, "time")
                if not time_file_path:
                    continue
                with open(time_file_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        print(line.strip())
                        with open(times_file_path, "w") as f:
                            f.write(line)
                            f.close

        # Call the function to list directories
        time_scraper(path)
    else:
        print("The provided path does not exist.")
