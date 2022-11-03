class FooBar {

  def name

  // エントリポイント
  static main(args) {
    def foobar = new FooBar()
    foobar.sayHello()
    println foobar.nextAge(22)
  }

  // コンストラクタ
  def FooBar() {
    name = "hoge"
  }

  // 普通のインスタンスメソッド
  def sayHello() {
    println "Hello ${name} !!"
  }

  String nextAge(Integer age) {
    "next age is ${age + 1}"
  }
}
