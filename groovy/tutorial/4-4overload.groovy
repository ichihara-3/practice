class Value {/*Test用クラス*/}

class Hoge {

  def test(String a) {
    "This is String"
  }

  def test(Integer a) {
    "This is Integer"
  }

  def test(Value a) {
    "This is Value Object"
  }
}


def obj = new Hoge()
assert obj.test(111) == "This is Integer"
assert obj.test("a") == "This is String"
assert obj.test(new Value()) == "This is Value Object"
