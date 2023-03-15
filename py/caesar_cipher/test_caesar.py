# 次のような入力を受け取り、結果をコンソールに出力する
# in: String, Shift(Int)
# out: Caesar Encoded String by Shift
# 例: python3 caesar.py "abc" 1
#     bcd
# 例: python3 caesar.py "abc" 2
#     cde

from caesar import caesar


def test_caeasar():
    assert caesar("abc", 0) == "abc"
    assert caesar("abc", 1) == "bcd"
    assert caesar("abc", -1) == "zab"
    assert caesar("abc", 26) == "abc"
    assert caesar("abc", 27) == "bcd"
    assert caesar("abc", -27) == "zab"
    assert caesar("abc", 52) == "abc"
    assert caesar("ABC", 1) == "BCD"
    assert caesar("本日は晴天也abc", 1) == "本日は晴天也bcd"
