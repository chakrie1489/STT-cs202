#!/bin/bash

# Set timeout duration in seconds
TIMEOUT_DURATION=210  

# Log file for skipped files
SKIPPED_LOG="skipped_files.log"
echo "Skipped Files Log" > $SKIPPED_LOG
echo "=================" >> $SKIPPED_LOG

# Read file paths (skipping first line)
tail -n +2 low_coverage_files.txt | while read file; do
    module_name=$(echo $file | sed 's/\//./g' | sed 's/.py$//')
    echo "Generating tests for $module_name"

    # Run Pynguin with timeout and capture errors
    ERROR_OUTPUT=$(timeout $TIMEOUT_DURATION pynguin --project-path . --module-name $module_name --output-path generated_tests/ 2>&1)

    # Check exit status
    EXIT_CODE=$?

    if [[ $EXIT_CODE -eq 124 ]]; then
        echo "Skipping $module_name due to timeout!"
        echo "$module_name - Skipped due to timeout" >> $SKIPPED_LOG
    elif [[ $EXIT_CODE -ne 0 ]]; then
        echo "Skipping $module_name due to an error!"
        echo "$module_name - Skipped due to error: $ERROR_OUTPUT" >> $SKIPPED_LOG
    fi
done
