import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load coverage JSON report
with open("coverage_existing.json") as f:
    data = json.load(f)

# Extract coverage percentages
coverage = [metrics["summary"]["percent_covered"] for metrics in data["files"].values()]

# Bin coverage into categories
bins = [0, 20, 40, 60, 80, 100]
labels = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
df = pd.DataFrame({"Coverage": pd.cut(coverage, bins=bins, labels=labels)})

# Count files in each bin
coverage_counts = df["Coverage"].value_counts().sort_index()

# Plot bar chart
plt.figure(figsize=(8, 5))
sns.barplot(x=coverage_counts.index, y=coverage_counts.values, palette="Blues_r")
plt.xlabel("Coverage Range (%)")
plt.ylabel("Number of Files")
plt.title("Distribution of Code Coverage Across Files")
plt.show()
