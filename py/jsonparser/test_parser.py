import parser
import pytest


class TestValues:
    def test_is_null(self):
        string = "null"
        assert parser.is_null(string) is True

        string = "true"
        assert parser.is_null(string) is False

    def test_is_true(self):
        string = "true"
        assert parser.is_true(string) is True

        string = "false"
        assert parser.is_true(string) is False

    def test_is_false(self):
        string = "false"
        assert parser.is_false(string) is True

        string = "true"
        assert parser.is_false(string) is False

    def test_is_string(self):
        string = '"valid"'
        assert parser.is_string(string) is True

        string = '"invalid1'
        assert parser.is_string(string) is False

        string = 'invalid2"'
        assert parser.is_string(string) is False

        string = "invalid3"
        assert parser.is_string(string) is False

    def test_is_array(self):
        string = "[valid]"
        assert parser.is_array(string) is True

        string = "[invalid1"
        assert parser.is_array(string) is False

        string = "invalid2]"
        assert parser.is_array(string) is False

        string = "invalid3"
        assert parser.is_array(string) is False

    def test_is_object(self):
        string = '{"key": "valid"}'
        assert parser.is_object(string) is True

        string = '{"key": "invalid1"'
        assert parser.is_object(string) is False

        string = '"key": "invalid2"}'
        assert parser.is_object(string) is False

        string = "invalid3"
        assert parser.is_object(string) is False

    def test_is_number(self):
        string = "1"
        assert parser.is_number(string) is True

        string = '"1"'
        assert parser.is_number(string) is False

        string = "-1"
        assert parser.is_number(string) is True

        string = "-0"
        assert parser.is_number(string) is True

        string = "-1.1"
        assert parser.is_number(string) is True

        string = "-1.111"
        assert parser.is_number(string) is True

        string = "-1.111"
        assert parser.is_number(string) is True

        string = "-1.111e10"
        assert parser.is_number(string) is True

        string = "-1.111E10"
        assert parser.is_number(string) is True

        string = "1E10"
        assert parser.is_number(string) is True

        string = "1E10.10"
        assert parser.is_number(string) is False

        string = "1E"
        assert parser.is_number(string) is False

        string = "１Ｅ"
        assert parser.is_number(string) is False

        string = "-01"
        assert parser.is_number(string) is False

        string = "1."
        assert parser.is_number(string) is False

    def test_is_float(self):
        string = "1.0"
        assert parser.is_float(string) is True

        string = "-1.0e10"
        assert parser.is_float(string) is True

        string = "1"
        assert parser.is_float(string) is False

        string = '"xxxx"'
        assert parser.is_float(string) is False

    def test_is_int(self):
        string = "10"
        assert parser.is_int(string) is True

        string = "-100"
        assert parser.is_int(string) is True

        string = "10.5"
        assert parser.is_int(string) is False

        string = '"xxxx"'
        assert parser.is_int(string) is False


class TestParser:
    def test_int(self):
        p = parser.Parser()

        string = "1"
        expected = 1

        result = p.parse(string)
        assert result == expected

    def test_int_surrounded_by_ws(self):
        p = parser.Parser()

        string = "\t\r\n 1 \t\r\n "
        expected = 1

        result = p.parse(string)
        assert result == expected

    def test_float(self):
        p = parser.Parser()
        string = "1.5"
        expected = 1.5

        result = p.parse(string)

        assert result == expected

    def test_float_surrounded_by_ws(self):
        p = parser.Parser()
        string = " \t\r\n1.5 \t\r\n     "
        expected = 1.5

        result = p.parse(string)

        assert result == expected

    def test_str(self):
        p = parser.Parser()
        string = '"string"'
        expected = "string"

        result = p.parse(string)

        assert result == expected

    def test_str_surrounded_by_ws(self):
        p = parser.Parser()
        string = ' \t\r\n "string" \t\r\n     '
        expected = "string"

        result = p.parse(string)

        assert result == expected

    def test_str_with_escape(self):
        p = parser.Parser()
        string = r'"\" \\ \/ \b \f \n \r \t \uFFFF\u1234"'
        expected = '" \\ / \b \f \n \r \t \uFFFF\u1234'

        result = p.parse(string)

        assert result == expected

    def test_empty_str(self):
        p = parser.Parser()
        string = '""'
        expected = ""

        result = p.parse(string)

        assert result == expected

    def test_null(self):
        p = parser.Parser()
        string = "null"
        expected = None

        result = p.parse(string)

        assert result == expected

    def test_null_surrounded_by_ws(self):
        p = parser.Parser()
        string = " \t\r\n null \t\r\n "
        expected = None

        result = p.parse(string)

        assert result == expected

    def test_true(self):
        p = parser.Parser()
        string = "true"
        expected = True

        result = p.parse(string)

        assert result == expected

    def test_true_surrounded_by_ws(self):
        p = parser.Parser()
        string = " \t\r\n true \t\r\n "
        expected = True

        result = p.parse(string)

        assert result == expected

    def test_false(self):
        p = parser.Parser()
        string = "false"
        expected = False

        result = p.parse(string)

        assert result == expected

    def test_false_surrounded_by_ws(self):
        p = parser.Parser()
        string = " \t\r\n false \t\r\n "
        expected = False

        result = p.parse(string)

        assert result == expected

    def test_empty_array(self):

        p = parser.Parser()
        string = "[]"
        expected = []

        result = p.parse(string)

        assert result == expected

    def test_int_in_array(self):
        p = parser.Parser()
        string = "[1,10]"
        expected = [1, 10]

        result = p.parse(string)

        assert result == expected

    def test_str_in_array(self):
        p = parser.Parser()
        string = '["a","helloworldxxx"]'
        expected = ["a", "helloworldxxx"]

        result = p.parse(string)

        assert result == expected

    def test_values_in_array(self):
        p = parser.Parser()
        string = "[null,true,false]"
        expected = [None, True, False]

        result = p.parse(string)

        assert result == expected

    def test_array_with_ws(self):
        p = parser.Parser()
        string = "\n  \t \r [ \n\r\t null \r \t \n ,\r\n\t true \r\n\t ,        false \t\t\t\t\t\t\r\n]    \r\n"
        expected = [None, True, False]

        result = p.parse(string)

        assert result == expected

    def test_array_in_array(self):
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

    def test_empty_object(self):
        p = parser.Parser()
        string = "{}"
        expected = {}

        result = p.parse(string)

        assert result == expected

    def test_object_one_pair_str(self):
        p = parser.Parser()
        string = '{"key": "value"}'
        expected = {"key": "value"}

        result = p.parse(string)

        assert result == expected

    def test_object_one_pair_int(self):
        p = parser.Parser()
        string = '{"key": 1234}'
        expected = {"key": 1234}

        result = p.parse(string)

        assert result == expected

    def test_object_one_pair_float(self):
        p = parser.Parser()
        string = '{"key": -1234.56e78}'
        expected = {"key": -1234.56e78}

        result = p.parse(string)

        assert result == expected

    def test_invalid_literal(self):
        p = parser.Parser()
        string = "1a2b3c"
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = r'"\a\b\c\d"'
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = r'"\u123"'
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = r'"\"'
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = r'"\uXXXX"'
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = "[1,2,3,"
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = "{1:"
        with pytest.raises(ValueError):
            p.parse(string)
