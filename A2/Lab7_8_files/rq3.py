import json
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Bandit CWE Mappings
BANDIT_CWE_MAPPINGS = {
    "B101": "CWE-338",  # Use of weak random generator
    "B102": "CWE-798",  # Hardcoded password
    "B103": "CWE-321",  # Use of temp file without secure options
    "B104": "CWE-732",  # Unrestricted file access
    "B105": "CWE-798",  # Hardcoded passwords
    "B106": "CWE-798",  # Hardcoded passwords
    "B107": "CWE-798",  # Hardcoded passwords in string
    "B108": "CWE-200",  # Information exposure
    "B110": "CWE-829",  # Pickle module usage (possible remote execution)
    "B112": "CWE-78",   # Use of eval()
    "B201": "CWE-242",  # Use of exec()
    "B301": "CWE-327",  # Use of weak hashing function (md5, sha1)
    "B302": "CWE-326",  # Use of insufficiently secure cipher mode
    "B303": "CWE-327",  # Use of insecure cipher
    "B304": "CWE-327",  # Use of insecure hash function
    "B305": "CWE-327",  # Use of insecure cipher (Blowfish, DES, RC2, etc.)
    "B306": "CWE-276",  # Improper file permissions
    "B307": "CWE-269",  # Insecure YAML loading
    "B308": "CWE-732",  # Insecure file permissions
    "B309": "CWE-610",  # SQL statement constructed with string formatting
    "B310": "CWE-78",   # Use of subprocess with shell=True (Command Injection)
    "B311": "CWE-78",   # Use of os.system() (Command Injection)
    "B312": "CWE-78",   # Use of popen functions (Command Injection)
    "B313": "CWE-78",   # Use of input() in Python 2
    "B314": "CWE-89",   # Possible SQL injection
    "B315": "CWE-117",  # Improper log handling (user-controlled input)
    "B316": "CWE-703",  # Incorrect error handling
    "B317": "CWE-502",  # Deserialization of untrusted data
    "B318": "CWE-327",  # Use of weak cryptographic algorithm
    "B319": "CWE-326",  # Use of weak cipher
    "B320": "CWE-798",  # Hardcoded cryptographic key
    "B321": "CWE-502",  # Unsafe XML deserialization
    "B322": "CWE-23",   # Path traversal vulnerability
    "B323": "CWE-200",  # Information exposure through debug mode
    "B324": "CWE-312",  # Storing passwords in plaintext
    "B325": "CWE-732",  # Incorrect file permission settings
}

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
                    issue_code = issue.get("test_id", "")
                    if issue_code in BANDIT_CWE_MAPPINGS:
                        cwe_counter[BANDIT_CWE_MAPPINGS[issue_code]] += 1
        
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
plt.title("Comparison of CWE Frequencies Across Repositories")
plt.xticks(x + bar_width, top_cwes, rotation=45)
plt.legend(title="Repositories")
plt.grid(axis="y")
plt.show()
