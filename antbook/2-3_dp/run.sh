#!/bin/bash
set -e
for f in $(ls ./testcases/*.txt |sort -t t -k 2 -n) ; do
  echo ${f}; cat ${f} | time python3 solve_fullsearch.py
  echo --------
done
