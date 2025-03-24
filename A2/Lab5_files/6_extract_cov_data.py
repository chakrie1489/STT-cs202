import xml.etree.ElementTree as ET

# Load coverage reports
tree_A = ET.parse('coverage_suite_A.xml')
tree_B = ET.parse('coverage_suite_B.xml')

root_A = tree_A.getroot()
root_B = tree_B.getroot()

# Read the list of files tested in Test Suite B
with open("low_coverage_files.txt") as f:
    files_to_check = [line.strip() for line in f.readlines()][1:]  # Skip header line

coverage_data = []

# Extract coverage info for relevant files
for filename in files_to_check:
    file_A = root_A.find(f".//class[@filename='{filename}']")
    file_B = root_B.find(f".//class[@filename='{filename}']")

    if file_B is not None:  # Only consider files where Suite B has coverage data
        coverage_B = float(file_B.get('line-rate')) * 100
        
        if coverage_B > 0:  # Skip files where coverage is still 0%
            coverage_A = float(file_A.get('line-rate')) * 100 if file_A is not None else 0
            coverage_data.append(f"{filename}: A = {coverage_A:.2f}%, B = {coverage_B:.2f}%")

# Save results
with open("coverage_results.txt", "w") as f:
    f.write("\n".join(coverage_data))

print("Filtered coverage results saved to coverage_results.txt")
