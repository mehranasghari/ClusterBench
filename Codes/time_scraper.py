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
        # Function to list directories
        def time_scraper(path):
            for dirnames in os.walk(path):
                for dirname in dirnames:
                    print(dirname)

        # Call the function to list directories
        time_scraper(path)
    else:
        print("The provided path does not exist.")
