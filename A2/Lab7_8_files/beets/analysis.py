import os
import json
import csv

# Full CWE Mapping for Bandit Issue Codes
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

# Path to the folder containing Bandit reports
reports_folder = "bandit_reports"

# Store analysis results
summary = {}

# Loop through each Bandit report
for report_file in os.listdir(reports_folder):
    if report_file.endswith(".json"):
        commit_hash = report_file.split("_")[1].split(".")[0]  # Extract commit hash
        with open(os.path.join(reports_folder, report_file), "r") as f:
            data = json.load(f)

        # Initialize counters
        severity_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        confidence_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        unique_cwes = set()

        # Process vulnerabilities
        for issue in data.get("results", []):
            severity_count[issue["issue_severity"]] += 1
            confidence_count[issue["issue_confidence"]] += 1
            
            # Get issue code (e.g., "B101") and map to CWE
            issue_code = issue.get("test_id", "")
            if issue_code in BANDIT_CWE_MAPPINGS:
                unique_cwes.add(BANDIT_CWE_MAPPINGS[issue_code])

        # Store results for this commit
        summary[commit_hash] = {
            "severity": severity_count,
            "confidence": confidence_count,
            "cwes": list(unique_cwes),
        }

# Write results to CSV file
csv_file = "bandit_analysis_results.csv"
with open(csv_file, 'w', newline='') as f:
    fieldnames = [
        'Commit', 
        'HIGH Severity', 'MEDIUM Severity', 'LOW Severity',
        'HIGH Confidence', 'MEDIUM Confidence', 'LOW Confidence',
        'Unique CWEs'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for commit, result in summary.items():
        writer.writerow({
            'Commit': commit,
            'HIGH Severity': result['severity']['HIGH'],
            'MEDIUM Severity': result['severity']['MEDIUM'],
            'LOW Severity': result['severity']['LOW'],
            'HIGH Confidence': result['confidence']['HIGH'],
            'MEDIUM Confidence': result['confidence']['MEDIUM'],
            'LOW Confidence': result['confidence']['LOW'],
            'Unique CWEs': ', '.join(result['cwes'])
        })

print(f"Analysis results have been written to {csv_file}")
