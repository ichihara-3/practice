assert [1,2,3,4,5,6].findAll {it % 2 != 0} == [1, 3, 5]
assert [1,2,3].findAll { it % 2 == 0} == [2]
