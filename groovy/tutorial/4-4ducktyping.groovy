class Value1{ def test() {"This is Value1 Object"}}
class Value2{ def test() {"This is Value2 Object"}}

class Hoge2 {
  def test(a) {
    a.test()
  }
}


def obj2 = new Hoge2()


assert obj2.test(new Value1()) == "This is Value1 Object"
assert obj2.test(new Value2()) == "This is Value2 Object"
