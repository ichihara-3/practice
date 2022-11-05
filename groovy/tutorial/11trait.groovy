// http://docs.groovy-lang.org/next/html/documentation/core-traits.html
trait Human {
  String name = "taro3"
  public Integer age = 31
  private twitter = "@ichi_taro3"
  public String speak() {
    "I am Human"
  }
  // public、もしくはフィールドを宣言すると、ゲッターとセッターを用意するか、特殊な記法でアクセスする必要がある
  // ただし、アクセサメソッドを実装すると、専用記法(xxx.Human__age)が利用できなくなる
  public Integer getAge(){
    age
  }
  public String getTwitter() {
    twitter
  }
}

class Man implements Human {}

def man = new Man()
assert "I am Human" == man.speak()
assert "taro3" == man.name
assert 31 == man.age
assert "@ichi_taro3" == man.Human__twitter
assert "@ichi_taro3" == man.twitter


// 複数のtraitをimplementsして、同名のメソッドがある場合は、implementsの右側が優先される
trait AA {String exec() {"A"}}
trait BB {String exec() {"B"}}
trait CC {String exec() {"C"}}
class DD implements AA, BB, CC {}
def d = new DD()
assert "C" == d.exec()


interface AAA {String exec()}

class BBB implements AAA {
  String exec(){"BBBBBBBBBB"}
}

def b = new BBB()
println b.exec()

// https://www.slideshare.net/uehaj/groovy-trait
trait R { String whoami() {"R ->" + super.whoami()}}
trait B1 extends R { String whoami() {"B1 ->" + super.whoami()}}
trait B2 extends R { String whoami() {"B2 ->" + super.whoami()}}
trait C1 extends B1 { String whoami() {"C1 ->" + super.whoami()}}
trait C2 extends B1 { String whoami() {"C2 ->" + super.whoami()}}
trait C3 extends B2 { String whoami() {"C3 ->" + super.whoami()}}
trait C4 extends B2 { String whoami() {"C4 ->" + super.whoami()}}
class D implements C4, C3, R, C2, C1 { String whoami(){"D"}}
class E extends D implements C1, C2, C3, C4 {}
m = new E()
n = new D()
println m.whoami()
println n.whoami()
