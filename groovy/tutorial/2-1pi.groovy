def pi = {Integer k, Integer to, Closure exp ->
  (k..to).collect{
    exp(it)
  }.inject {l, r ->
    l * r
  }
}

assert 120 == pi(1, 4){it + 1}
