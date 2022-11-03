String npe = null
Optional<String> nptOpt = Optional.ofNullable(npe)
assert 0 == nptOpt.map {it.toInteger() * 2}.orElse(0)

assert Optional.empty() == Optional.ofNullable(null).filter{it % 2 == 0}
assert Optional.empty() == Optional.ofNullable(1).filter{it % 2 == 0}
assert Optional.empty() != Optional.ofNullable(2).filter{it % 2 == 0}
assert Optional.ofNullable(2) == Optional.ofNullable(2).filter{it % 2 == 0}
