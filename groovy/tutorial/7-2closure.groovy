class Test {
  static getClosure() {
    Integer defaultCount = 0
    return {
      defaultCount++
      defaultCount
    }
  }
}

Closure clj = Test.getClosure()
assert 1 == clj()
assert 2 == clj()
assert 3 == clj()

Closure clj2 = Test.getClosure()
assert 1 == clj2()
assert 2 == clj2()
assert 4 == clj()

