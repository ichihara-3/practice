(1..100).collect {
  it % 15 == 0 ? "FizzBuzz" : it
}.collect {
  (it instanceof Integer) && it % 3 == 0 ? "Fizz" : it
}.collect {
  (it instanceof Integer) && it % 5 == 0 ?  "Buzz" : it
}.collect {
  println it
}
