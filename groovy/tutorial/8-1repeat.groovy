Map map = [foo:"bar", bar:"foo"]
map.each {
  println it
}

map.each {
  println "key = ${it.key}, value = ${it.value}"
}
