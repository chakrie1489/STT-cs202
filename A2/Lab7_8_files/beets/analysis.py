import os
import json
import csv

reports_folder = "bandit_reports"
summary = {}

for report_file in os.listdir(reports_folder):
    if report_file.endswith(".json"):
        commit_hash = report_file.split("_")[1].split(".")[0]  # Extract commit hash
        with open(os.path.join(reports_folder, report_file), "r") as f:
            data = json.load(f)
        severity_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        confidence_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        unique_cwes = set()
        
        for issue in data.get("results", []):
            severity_count[issue["issue_severity"]] += 1
            confidence_count[issue["issue_confidence"]] += 1
            
            # Extract CWE ID from issue_cwe field
            if "issue_cwe" in issue and "id" in issue["issue_cwe"]:
                unique_cwes.add(f'CWE-{issue["issue_cwe"]["id"]}')

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
