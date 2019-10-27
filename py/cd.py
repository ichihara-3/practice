from math import sqrt, ceil

a, b = map(int, input().split())

def gcd(a, b):
  x, y = (a, b) if a > b else (b, a)
  while y > 0:
    x, y = y, x % y
  return x

d = gcd(a, b)
ans = 1
for i in range(2, ceil(sqrt(d))+1):
  if d % i == 0:
    ans += 1
    while(d % i == 0):
      d = d / i
if d != 1:
    ans += 1
print(ans)
