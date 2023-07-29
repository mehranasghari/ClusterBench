file_path = "./output.txt"
seen_lines = set()

with open(file_path, "r") as f:
    lines = f.readlines()
    for line_number, line in enumerate(lines):
        # Remove leading/trailing whitespaces and newlines for comparison
        clean_line = line.strip()
        if clean_line in seen_lines:
            print("Duplicate found at line:", line_number + 1)
            break
        seen_lines.add(clean_line)
    else:
        print("No duplicates found.")
