import matplotlib.pyplot as plt
import numpy as np

# Read filtered coverage data
filenames, coverage_A, coverage_B = [], [], []
with open("coverage_results.txt") as f:
    for line in f:
        parts = line.strip().split(": A = ")
        filename = parts[0]
        cov_A, cov_B = map(float, parts[1].replace("%", "").split(", B = "))

        filenames.append(filename.split("/")[-1])  # Use only filename for readability
        coverage_A.append(cov_A)
        coverage_B.append(cov_B)

x = np.arange(len(filenames))  # X-axis positions

plt.figure(figsize=(10, 5))
plt.bar(x - 0.2, coverage_A, width=0.4, label="Test Suite A", color='blue')
plt.bar(x + 0.2, coverage_B, width=0.4, label="Test Suite B", color='green')

plt.xticks(x, filenames, rotation=90)
plt.xlabel("Files")
plt.ylabel("Coverage (%)")
plt.title("Coverage Comparison: Test Suite A vs. Test Suite B (Filtered)")
plt.legend()
plt.tight_layout()
plt.savefig("coverage_comparison_filtered.png")
plt.show()
