file_path = "./../conf/output.txt"
a, b, c, d, e = 0, 0, 0, 0, 0
seen_lines = set()

# Check for duplicate lines
with open(file_path, "r") as f:
    lines = f.readlines()
    for line_number, line in enumerate(lines):
        clean_line = line.strip()
        if clean_line in seen_lines:
            print("Duplicate found at line:", line_number + 1)
            break
        seen_lines.add(clean_line)
    else:
        print("No duplicates found.")

# Count occurrences of specific words
with open(file_path, "r") as f:
    lines = f.readlines()
    for line in lines:
        if "cpu" in line:
            a += 1
        if "disk" in line:
            b += 1
        if "memory" in line:
            c += 1
        if "mem" in line:
            d += 1
        if "ram" in line:
            e += 1

print("\n cpu count : ", a)
print(" disk count : ", b)
print(" memory count : ", c)
print(" mem count : ", d)
print(" ram count : ", e)
