Closure toInt = {String v ->
  v.toInteger()
}
Closure twice = {Integer v ->
  v * 2
}

// sample
Closure getDataFromDatabase = {
  "5"
}

assert 10 == twice(toInt(getDataFromDatabase()))


Closure calc1 = getDataFromDatabase >> toInt >> twice
Closure calc2 = twice << toInt << getDataFromDatabase

assert 10 == calc1()
assert 10 == calc2()

Closure getDataFromDatabase2 = {String a ->
  "5" + a
}
Closure calc3 = getDataFromDatabase2 >> toInt >> twice
assert 106 == calc3("3")

asert 106 == (getDataFromDatabase2 >> toInt >> twice).call("3")
