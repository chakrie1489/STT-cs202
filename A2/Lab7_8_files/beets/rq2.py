import json
import os
import matplotlib.pyplot as plt

reports_folder = "bandit_reports"
severity_timeline = {"HIGH": {}, "MEDIUM": {}, "LOW": {}}
report_files = sorted([f for f in os.listdir(reports_folder) if f.endswith(".json")])

# Process each Bandit report
for report_file in report_files:
    commit_hash = report_file.split("_")[1].split(".")[0]  # Extract commit hash
    
    with open(os.path.join(reports_folder, report_file), "r") as f:
        data = json.load(f)

    # Count vulnerabilities for each severity level
    for severity in ["HIGH", "MEDIUM", "LOW"]:
        severity_count = sum(1 for issue in data.get("results", []) if issue["issue_severity"] == severity)
        severity_timeline[severity][commit_hash] = severity_count

# Plot severity trends over time
plt.figure(figsize=(12, 6))

for severity in ["HIGH", "MEDIUM", "LOW"]:
    plt.plot(severity_timeline[severity].keys(), severity_timeline[severity].values(), 
             marker='o', linestyle='-', label=severity)

plt.xticks(rotation=90, fontsize=8)
plt.xlabel("Commits")
plt.ylabel("Number of Vulnerabilities")
plt.title("Vulnerability Trends by Severity Over Time - beets repo")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
