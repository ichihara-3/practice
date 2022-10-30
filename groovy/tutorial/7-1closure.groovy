Closure clj = {
  println "Hello Closure!"
}


Closure clj2 = {String name ->
  println "Hello ${name}"
}

def clj3 = {String place -> println "Hello ${place}"}

clj()
clj2("ichi_taro3")
clj2("World")


def reseach = [1,2,3].each {
  it * 2
}
println reseach
def rescollect = [1,2,3].collect {
  it * 2
}
println rescollect

List list = [1,2,3]
Closure doubled = {
  it * 2
}

assert [2,4,6] == list.collect(doubled)
