def a = 1
def b = 0.1
def c = "hello groovy"

println a
println a.getClass().getName()
println b
println b.getClass().getName()
println c
println c.getClass().getName()

// 中身を交換
a = c
println a
