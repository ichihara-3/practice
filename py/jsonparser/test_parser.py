import parser


def test_int():
    p = parser.Parser()

    string = '1'
    expected = 1

    result = p.parse(string)
    assert result == expected


def test_float():
    p = parser.Parser()
    string = '1.5'
    expected = 1.5

    result = p.parse(string)

    assert result == expected


def test_str():
    p = parser.Parser()
    string = '"string"'
    expected = "string"

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
    string = 'null'
    expected = None

    result = p.parse(string)

    assert result == expected


def test_empty_array():

    p = parser.Parser()
    string = '[]'
    expected = []

    result = p.parse(string)

    assert result == expected


def test_int_in_array():
    p = parser.Parser()
    string = '[1,10]'
    expected = [1, 10]

    result = p.parse(string)

    assert result == expected

