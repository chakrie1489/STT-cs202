import matplotlib.pyplot as plt

# Data from execution matrix
modes = ["Single Process (n=1)", "Auto Workers (n=auto)", "Single Thread (threads=1)", 
         "Auto Threads (threads_auto)", "Dist Load (dist=load)", "Dist No (dist=no)"]
execution_times = [3.06, 3.36, 2.85, 44.55, 3.32, 3.35]  # Avg. execution times in seconds
single_time = execution_times[0]  # Baseline for speedup calculation

# Compute speedup values
speedup_values = [single_time / t for t in execution_times]

# Plot
plt.figure(figsize=(8, 5))
plt.bar(modes, speedup_values, color=['blue', 'green', 'red', 'purple', 'orange', 'cyan'])
plt.xlabel("Parallelization Mode")
plt.ylabel("Speedup (Relative to Single Process)")
plt.title("Speedup Comparison for Different Parallelization Modes")
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 1.2)  # Keeping limits reasonable
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()
