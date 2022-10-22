class Hoge {
  Hoge() {
    println "Constructor"
  }

  def piyo(value) {
    println value
  }
}

def hoge = new Hoge()
hoge.piyo("this is my value")
hoge.piyo(12345)
