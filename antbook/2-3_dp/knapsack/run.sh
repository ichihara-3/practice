#!/bin/bash
set -e
script=${1:-solve_fullsearch.py}
for f in $(ls ./testcases/*.txt |sort -t t -k 2 -n) ; do
  echo ${f}; cat ${f} | time python3 ${script}
  echo --------
done
