#!/bin/bash
result=$(echo test |nc -w 1 127.0.0.1 7 )
if [[ ${result} != test ]]; then
  echo result = \"${result}\", expected: test
fi
