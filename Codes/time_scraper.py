import os
import argparse

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

        # Function to scrape time information
        def time_scraper(path):
            with open(times_file_path, "w") as output_file:
                for dirpath, dirnames, filenames in os.walk(path):
                    for dirname in dirnames:
                        time_file_path = os.path.join(dirpath, dirname, "time")
                        if os.path.exists(time_file_path):
                            with open(time_file_path, "r") as input_file:
                                lines = input_file.readlines()
                                for line in lines:
                                    output_file.write(line.strip() + "\n")  # Add newline

        # Call the function to scrape and save time information
        time_scraper(path)
        print(f"Time information scraped and saved to {times_file_path}")
    else:
        print("The provided path does not exist.")
