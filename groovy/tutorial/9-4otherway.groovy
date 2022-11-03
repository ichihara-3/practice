def list = []
assert "empty" == list ? list.head() : 'empty'

list = ["yeay"]
assert "yeay" == list ? list.head() : 'empty'


// GroovyでもメタプログラミングでListに機能を追加すればよりスマートに表現できる！
// ListクラスにorElseメソッドを追加
List.metaClass.orElse = {def alternativeValue ->
  delegate ? delegate.head() : alternativeValue
}

assert "yeay" == list.orElse(99)
list = []
assert 99 == list.orElse(99)
assert 'java.lang.Integer' == list.orElse(99).class.name
