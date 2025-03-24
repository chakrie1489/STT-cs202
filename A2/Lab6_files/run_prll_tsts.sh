#!/bin/bash

# Define the number of repetitions per configuration
REPS=3
LOG_DIR="test_logs"
mkdir -p "$LOG_DIR"

# File to store execution times
EXEC_TIME_FILE="$LOG_DIR/execution_times.txt"
FLAKY_TESTS_FILE="$LOG_DIR/failing_tests.txt"

# Clear previous logs
> "$EXEC_TIME_FILE"
> "$FLAKY_TESTS_FILE"

# Function to run tests and log execution time & failures
run_tests() {
    CONFIG_NAME=$1
    CMD=$2
    LOG_FILE="$LOG_DIR/${CONFIG_NAME}.log"
    TIME_SUM=0

    echo "Running tests for configuration: $CONFIG_NAME"
    > "$LOG_FILE"  # Clear previous log

    for i in $(seq 1 "$REPS"); do
        echo "Iteration $i for $CONFIG_NAME..." | tee -a "$LOG_FILE"

        # Execute test and measure execution time (capturing time in seconds)
        START_TIME=$(date +%s.%N)
        eval "$CMD" &>> "$LOG_FILE"
        END_TIME=$(date +%s.%N)

        # Compute execution time for this run
        EXEC_TIME=$(echo "$END_TIME - $START_TIME" | bc)
        TIME_SUM=$(echo "$TIME_SUM + $EXEC_TIME" | bc)

        # Capture failed test cases
        FAILURES=$(grep -E 'FAILED' "$LOG_FILE" | awk '{print $2}' | sort | uniq)
        echo "Iteration $i - Failed Tests:" >> "$FLAKY_TESTS_FILE"
        echo "$FAILURES" >> "$FLAKY_TESTS_FILE"
    done

    # Compute and store average execution time (Tpar)
    AVG_TIME=$(echo "scale=2; $TIME_SUM / $REPS" | bc)
    echo "$CONFIG_NAME: $AVG_TIME seconds" >> "$EXEC_TIME_FILE"
}

# Parallel Execution Configurations

# Process-level parallelization (pytest-xdist)
run_tests "n1" "pytest -n 1 --tb=short --disable-warnings"
run_tests "n_auto" "pytest -n auto --tb=short --disable-warnings"

# Thread-level parallelization (pytest-run-parallel)
run_tests "threads1" "pytest --parallel-threads=1 --tb=short --disable-warnings"
run_tests "threads_auto" "pytest --parallel-threads=auto --tb=short --disable-warnings"

# Different pytest-xdist distribution modes
run_tests "dist_load" "pytest -n auto --dist load --tb=short --disable-warnings"
run_tests "dist_no" "pytest -n auto --dist no --tb=short --disable-warnings"

# Consolidate failing test cases from all logs
echo "Final Consolidated Failing Tests:" >> "$FLAKY_TESTS_FILE"
grep -E 'FAILED' "$LOG_DIR"/*.log | awk '{print $2}' | sort | uniq -c >> "$FLAKY_TESTS_FILE"

echo "✅ Parallel test execution completed. Results stored in '$LOG_DIR'."
