import copy
import random
import io
import sys


n = random.randint(2, 2*(10**5))

A = list(range(1, n+1))
random.shuffle(A)
orgA=copy.copy(A)

#n = int(input())
#A = list(map(int, input().split()))

result = []
for i in range(n):
  j = A[i] -1
  while i != j:
    move = (i, j) if i < j else (j, i)
    result.append(move)
    A[i], A[j] = A[j], A[i]
    i = j

# print(len(result))
# for i, j in result:
#   print(i+1, j+1)

A = copy.copy(orgA)
for i, j in result:
    A[i], A[j] = A[j], A[i]


for a, b, in zip(A, sorted(orgA)):
    assert a == b, f"{a} != {b}"

