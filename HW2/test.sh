#!/bin/bash

echo "Building index... "
time python3 index.py -i /Users/tim/nltk_data/corpora/reuters/training -d dictionary.txt -p postings.txt
echo
echo "Testing correctness of indexing... "
time python3 test_index.py

