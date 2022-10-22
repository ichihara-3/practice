class Value {/*Test用クラス*/}

class Hoge {

  def test(a) {
    "This is String"
  }

  def test(a) {
    "This is Integer"
  }

  def test(a) {
    "This is Value Object"
  }
}


def obj = new Hoge()
assert obj.test(111) == "This is Integer"
assert obj.test("a") == "This is String"
assert obj.test(new Value()) == "This is Value Object"
