class A {
  def hoge() {
    println "A"
  }
}


class B {
  def hoge() {
    println "B"
  }
}

def a = new A()
def b = new B()

a.hoge()
b.hoge()
