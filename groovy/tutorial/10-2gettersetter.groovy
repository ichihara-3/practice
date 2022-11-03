class HogeXX {
  String name

  HogeXX(String name) {
    this.name = name
  }

  def setName(String name) {
    this.name = "${name}!!"
  }

  def getName() {
    "${name}!!"
  }
}

def hoge = new HogeXX("XXXX")
assert hoge.name == "XXXX!!"

hoge.name = "YYYY"
assert hoge.name == "YYYY!!!!"
