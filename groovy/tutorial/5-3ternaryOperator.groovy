def value = 1
def result = value ? "This is 1" : "This is not 1"

println result
assert result == "This is 1"
value = 0
result = value ? "This is 1" : "This is not 1"
println result
assert result == "This is not 1"
