// without elvis operator ?:(
def value = "aaa"
assert "aaa" == (value == "aaa" ? "aaa" : "not equal")

// with elvis operatro ?:)
def value2 = "bbb"
assert "bbb" == value2 ?: "not equal"
