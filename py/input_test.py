import timeit
import sys


print('input(): ', timeit.timeit('input()', number=2000000))
print('sys.stdin.readline()',timeit.timeit('sys.stdin.readline()', number=2000000))
