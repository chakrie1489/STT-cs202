#!/bin/bash

# Script to measure sequential test execution time
cd /home/pakambo/Documents/6th sem/cse202/lab6/algorithms/

echo "Running sequential test suite 3 times..."
total_time=0

for i in {1..3}; do
  echo "Run $i started at $(date)"
  start_time=$(date +%s.%N)
  python -m pytest
  end_time=$(date +%s.%N)
  execution_time=$(echo "$end_time - $start_time" | bc)
  total_time=$(echo "$total_time + $execution_time" | bc)
  echo "Run $i completed in $execution_time seconds"
done

average_time=$(echo "scale=4; $total_time / 3" | bc)
echo "Average execution time (Tseq): $average_time seconds"
echo "Tseq = $average_time seconds"