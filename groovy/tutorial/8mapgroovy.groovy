Map map = [foo:"bar", bar:"foo"]

// 値の取り出し
assert map.foo == "bar"
assert map.get("foo")
assert map["foo"] == "bar"
assert map.bar == "foo"

// 値の上書き
map["bar"] = "foo_updated"
assert map.bar == "foo_updated"
map.put("bar", "foo_updated2")
assert map.bar == "foo_updated2"


// 値の追加
assert map.size() == 2
map["hoge"] = "hoge_value"
assert map.size() == 3
assert map.hoge == "hoge_value"

map.put("piyo", "piyo_value")
assert map.size() == 4
assert map.piyo == "piyo_value"
