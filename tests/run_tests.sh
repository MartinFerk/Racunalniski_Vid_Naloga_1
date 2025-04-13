#!/bin/bash
echo "Running tests..."
python3 -m unittest discover tests > result.log
if grep -q "FAILED" result.log; then
    echo "Tests failed!" > napaka.txt
    exit 1
else
    echo "All tests passed!"
    exit 0
fi
