class Test2 {
  // normal closure
  Closure a = {
    println "普通のクロージャ"
    println " this:     ${this.class.name}"
    println " owner:    ${owner.class.name}"
    println " delegate: ${delegate.class.name}";


    {->
      println "クロージャの中のクロージャ"
      println " this:     ${this.class.name}"
      println " owner:    ${owner.class.name}"
      println " delegate: ${delegate.class.name}";
        {->
          println "クロージャの中のクロージャの中のクロージャ"
          println " this:     ${this.class.name}"
          println " owner:    ${owner.class.name}"
          println " delegate: ${delegate.class.name}"
        }()
    }()
  }
}


def test = new Test2()
test.a()


class Test3 {
  String abc = "Test3"
  def exec(Closure a) {
    a()
  }
}

class Foo {

  static main() {

      String abc = "ConsoleScript"
      def test3 = new Test3()

      // 凄い普通。abcという変数の中身を返すクロージャ
      // cls1が"実行されるときに"Hoge#main()で宣言している変数abcを参照するので、言うまでもなく変数abcを宣言しておかないとエラーになる。
      Closure cls1 = { -> abc }
      assert test3.exec( cls1 ) == "ConsoleScript"


      // これが応用バージョン
      // delegateを明示的に指定して、さらにクロージャ自身のdelegateにtest2インスタンスを
      // 指定することで、クロージャを渡した先(test2)の変数abcが参照されるようになる。
      // "Hoge#main()で宣言している変数abc"は使用しないので、このパターンだけで良ければHoge#main()の中の変数abcは削除しても大丈夫。
      Closure cls2 = { -> delegate.abc }
      cls2.delegate = test3
      assert test3.exec( cls2 ) == "Test3"
  }
}


Foo.main()
