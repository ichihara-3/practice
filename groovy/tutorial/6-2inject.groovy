assert [1,2,3].inject{a, b -> a+b} == 6

assert [5,3,6,10,8,0,1].inject {a, b ->
  a > b ? a : b
} == 10
