def sigma = {Integer k, Integer to, Closure exp ->
  (k..to).collect {
    exp(it)
  }.sum()
}
// カリー化してクロージャを渡してる
assert 25 == sigma(1, 5) {it + 2}
