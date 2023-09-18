import subprocess

class bcolors:
    YELLOW = '\033[1;33m'
    END = '\033[0m'
    
def run_script(script_path, xml_path, a_number):
    try:
        subprocess.check_call(["python3", script_path, xml_path, str(a_number)])
        print(f"Script {bcolors.YELLOW}{script_path}{bcolors.END} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

if __name__ == "__main__":
    input_file = "wl-address.txt"

    with open(input_file, "r") as file:
        lines = file.readlines()

    if len(lines) % 3 != 0:
        print("Error: Input file should have sets of three lines (script path, XML path, and number).")
        exit(1)

    for i in range(0, len(lines), 3):
        script_path = lines[i].strip()
        xml_path = lines[i + 1].strip()
        a_number = int(lines[i + 2].strip())

        run_script(script_path, xml_path, a_number)
