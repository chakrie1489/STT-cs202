for i in {1..10}; do
    echo "Running Sequential Test - Iteration $i"
    pytest --tb=short --disable-warnings | tee -a sequential_tests.log
done
