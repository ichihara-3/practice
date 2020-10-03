import parser


def test_int():
    p = parser.Parser()

    string = "1"
    expected = 1

    result = p.parse(string)
    assert result == expected


def test_int_surrounded_by_ws():
    p = parser.Parser()

    string = "\t\r\n 1 \t\r\n "
    expected = 1

    result = p.parse(string)
    assert result == expected


def test_float():
    p = parser.Parser()
    string = "1.5"
    expected = 1.5

    result = p.parse(string)

    assert result == expected


def test_float_surrounded_by_ws():
    p = parser.Parser()
    string = " \t\r\n1.5 \t\r\n     "
    expected = 1.5

    result = p.parse(string)

    assert result == expected


def test_str():
    p = parser.Parser()
    string = '"string"'
    expected = "string"

    result = p.parse(string)

    assert result == expected


def test_str_surrounded_by_ws():
    p = parser.Parser()
    string = ' \t\r\n "string" \t\r\n     '
    expected = "string"

    result = p.parse(string)

    assert result == expected


def test_str_with_escape():
    p = parser.Parser()
    string = ""
    expected = Ellipsis

    result = p.parse(string)

    assert result == expected


def test_empty_str():
    p = parser.Parser()
    string = '""'
    expected = ""

    result = p.parse(string)

    assert result == expected


def test_null():
    p = parser.Parser()
    string = "null"
    expected = None

    result = p.parse(string)

    assert result == expected


def test_null_surrounded_by_ws():
    p = parser.Parser()
    string = " \t\r\n null \t\r\n "
    expected = None

    result = p.parse(string)

    assert result == expected


def test_true():
    p = parser.Parser()
    string = "true"
    expected = True

    result = p.parse(string)

    assert result == expected


def test_true_surrounded_by_ws():
    p = parser.Parser()
    string = " \t\r\n true \t\r\n "
    expected = True

    result = p.parse(string)

    assert result == expected


def test_false():
    p = parser.Parser()
    string = "false"
    expected = False

    result = p.parse(string)

    assert result == expected


def test_false_surrounded_by_ws():
    p = parser.Parser()
    string = " \t\r\n false \t\r\n "
    expected = False

    result = p.parse(string)

    assert result == expected


def test_empty_array():

    p = parser.Parser()
    string = "[]"
    expected = []

    result = p.parse(string)

    assert result == expected


def test_int_in_array():
    p = parser.Parser()
    string = "[1,10]"
    expected = [1, 10]

    result = p.parse(string)

    assert result == expected


def test_str_in_array():
    p = parser.Parser()
    string = '["a","helloworldxxx"]'
    expected = ["a", "helloworldxxx"]

    result = p.parse(string)

    assert result == expected


def test_values_in_array():
    p = parser.Parser()
    string = "[null,true,false]"
    expected = [None, True, False]

    result = p.parse(string)

    assert result == expected


def test_array_with_ws():
    p = parser.Parser()
    string = "\n  \t \r [ \n\r\t null \r \t \n ,\r\n\t true \r\n\t ,        false \t\t\t\t\t\t\r\n]    \r\n"
    expected = [None, True, False]

    result = p.parse(string)

    assert result == expected


def test_array_in_array():
    p = parser.Parser()
    string = """
    [1, 2, [
        1, [
            1, 2, [
                1, []
                ]
            ]
        ]
    ]"""
    expected = [1, 2, [1, [1, 2, [1, []]]]]

    result = p.parse(string)

    assert result == expected
