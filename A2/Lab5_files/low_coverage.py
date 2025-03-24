import json

with open("coverage_existing.json") as f:
    data = json.load(f)

low_coverage_files = [file for file, metrics in data["files"].items() if metrics["summary"]["percent_covered"] < 100]
with open("low_coverage_files.txt", "w") as output_file:
    output_file.write("Files needing more tests:\n")
    for file in low_coverage_files:
        output_file.write(f"{file}\n")

print(f"Results written to low_coverage_files.txt")
