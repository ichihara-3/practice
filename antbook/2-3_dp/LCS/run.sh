#!/bin/bash

set -e

script=${1:-solve_memo.py}
cd $(dirname 0)

for case in $(find testcases -type f|sort -n);do
  echo ${case}
  cat ${case} | time python3 ${script}
  echo -------
done

