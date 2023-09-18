import os
import argparse
from datetime import datetime

# Create an argument parser
argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--path", help="path to test dirs")
args = argParser.parse_args()
path = args.path

# Check if the path is provided
if not path:
    print("Please provide a path using the -p or --path argument.")
else:
    # Check if the provided path exists
    if os.path.exists(path):
        # Define the path for the output file
        times_file_path = os.path.join(path, "time.txt")

        # Function to scrape and sort time information
        def time_scraper_and_sort(path):
            time_list = []  # Store the lines in a list
            with open(times_file_path, "w") as output_file:
                for dirpath, dirnames, filenames in os.walk(path):
                    for dirname in dirnames:
                        time_file_path = os.path.join(dirpath, dirname, "time")
                        if os.path.exists(time_file_path):
                            with open(time_file_path, "r") as input_file:
                                lines = input_file.readlines()
                                time_list.extend(lines)  # Add lines to the list

            # Sort the list of times by datetime
            time_list.sort(key=lambda x: datetime.strptime(x.strip(), "%Y-%m-%d %H:%M:%S"))

            # Write the sorted lines back to the file
            with open(times_file_path, "w") as output_file:
                output_file.writelines(time_list)

        # Call the function to scrape and sort time information
        time_scraper_and_sort(path)
        print(f"Time information scraped, sorted, and saved to {times_file_path}")
    else:
        print("The provided path does not exist.")
