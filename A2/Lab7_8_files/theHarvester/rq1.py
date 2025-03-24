import json
import os
import matplotlib.pyplot as plt

reports_folder = "bandit_reports"
high_severity_timeline = {}

# Process each Bandit report
for report_file in sorted(os.listdir(reports_folder)):
    if report_file.endswith(".json"):
        commit_hash = report_file.split("_")[1].split(".")[0]  # Extract commit hash
        
        with open(os.path.join(reports_folder, report_file), "r") as f:
            data = json.load(f)

        high_severity_count = sum(1 for issue in data.get("results", []) if issue["issue_severity"] == "HIGH")
        high_severity_timeline[commit_hash] = high_severity_count

# Plot timeline of high-severity vulnerabilities
plt.figure(figsize=(10, 5))
plt.plot(high_severity_timeline.keys(), high_severity_timeline.values(), marker='o', linestyle='-')
plt.xticks(rotation=90)  # Rotate commit labels
plt.xlabel("Commits")
plt.ylabel("High Severity Vulnerabilities")
plt.title("High Severity Vulnerabilities Over Time - theHarvester repo")
plt.grid()
plt.show()
