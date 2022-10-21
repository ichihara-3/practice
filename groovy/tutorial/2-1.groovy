a = (1..10).findAll {
  it % 2 == 0
}.collect {
  it * 2
}.inject {l, r ->
  l*r
}

println a
