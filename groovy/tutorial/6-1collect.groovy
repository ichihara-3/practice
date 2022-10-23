assert [1, 2, 3].collect { it * 2 } == [2, 4, 6]


def list = [1, 2, 3]
def list2 = list.collect {
  it * 2
}

assert [1, 2, 3] == list
assert [2, 4, 6] == list2


// java paradigm
def list3 = [1,2,3]
def list4 = []
for (def i = 0; i < list.size(); i++) {
  list4.add( list[i] * 2 )
}

assert [1,2,3] == list3
assert [2,4,6] == list4
