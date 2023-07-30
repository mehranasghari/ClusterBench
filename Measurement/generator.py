# Define disk file path
disk_file_path = "./disks.txt"
metrics_file_path = "./metric.txt"

def measurement_generator(input_value):
    match input_value:
        case "1":
            print("You chose ops.")
            with open(disk_file_path, "r") as file:
                disks = file.readlines()
                for disk in disks:
                    with open(metrics_file_path, "a") as metrics_file:
                        metrics_file.write(f"netdata.disk_ops.{disk.strip()}.reads\n")
                        metrics_file.write(f"netdata.disk_ops.{disk.strip()}.write\n")
        case "2":
            print("You chose option 2.")
        case "3":
            print("You chose option 3.")
        case _:
            print("Invalid option.")

# Example usage:
print(''' HINT
1) OPS measurements(read and write) ''')
user_input = input("\n Enter your choice: ")
measurement_generator(user_input)