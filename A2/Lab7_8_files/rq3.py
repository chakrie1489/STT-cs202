import json
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Path to Lab 7 & 8 directory
lab_dir = os.path.expanduser("~/Documents/6th sem/cse202/lab7_8")

# Dictionary to store CWE counts per repository
repo_cwe_counts = {}

# Process each repository (beets, theHarvester, ChatTTS)
for repo_name in ["beets", "theHarvester", "ChatTTS"]:
    repo_path = os.path.join(lab_dir, repo_name, "bandit_reports")
    
    if os.path.isdir(repo_path):  # Ensure it's a directory
        cwe_counter = Counter()
        
        # Process each Bandit report in the repository folder
        for report_file in os.listdir(repo_path):
            if report_file.endswith(".json"):
                with open(os.path.join(repo_path, report_file), "r") as f:
                    data = json.load(f)

                for issue in data.get("results", []):
                    issue_cwe = issue.get("issue_cwe", {}).get("id")  # Extract CWE ID
                    if issue_cwe:
                        cwe_counter[issue_cwe] += 1
        
        repo_cwe_counts[repo_name] = dict(cwe_counter)

# Save CWE frequencies for each repository
output_path = os.path.join(lab_dir, "cwe_frequencies.json")
with open(output_path, "w") as f:
    json.dump(repo_cwe_counts, f, indent=4)

# Get the top 10 most common CWEs overall
all_cwe_counts = Counter()
for repo in repo_cwe_counts.values():
    all_cwe_counts.update(repo)
top_cwes = [cwe[0] for cwe in all_cwe_counts.most_common(10)]

# Plot CWE distributions across repositories
repo_names = list(repo_cwe_counts.keys())
bar_width = 0.2  # Width of bars for each repository
x = np.arange(len(top_cwes))  # X-axis positions

plt.figure(figsize=(12, 6))

# Plot bars for each repository
for i, repo in enumerate(repo_names):
    repo_counts = [repo_cwe_counts[repo].get(cwe, 0) for cwe in top_cwes]
    plt.bar(x + i * bar_width, repo_counts, width=bar_width, label=repo)

# Formatting the plot
plt.xlabel("CWE ID")
plt.ylabel("Frequency")
plt.title("Comparison of Top 10 CWE Frequencies Across Repositories")
plt.xticks(x + bar_width, top_cwes, rotation=45)
plt.legend(title="Repositories")
plt.grid(axis="y")
plt.show()
