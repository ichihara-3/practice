from textwrap import dedent
import parser
import pytest


class TestValues:

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

        string = "1E+10"
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

        string = "1.5e+10"
        expected = 1.5e10
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
        chars = {
            '"\\\x22"': '"',  # "     引用符                    U+0022
            '"\\\x5C"': "\\",  # \     バックスラッシュ          U+005C
            '"\\\x2F"': "/",  # /     スラッシュ                U+002F
            '"\\\x62"': "\b",  # b     バックスペース            U+0008
            '"\\\x66"': "\f",  # f     改ページ(Form feed)       U+000C
            '"\\\x6E"': "\n",  # n     改行(Line feed)           U+000A
            '"\\\x72"': "\r",  # r     復帰改行(Carriage return) U+000D
            '"\\\x74"': "\t",  # t     タブ                      U+0009
            '"\\\x75AAAA"': "\uAAAA",  # uXXXX                 U+XXXX
        }
        for char, expected in chars.items():
            result = p.parse(char)

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

    def test_object_multiple_members(self):
        p = parser.Parser()
        string = '{"int": 1234, "float": -1234.56e78, "str": "onetwothreefour"}'
        expected = {"int": 1234, "float": -1.23456e81, "str": "onetwothreefour"}

        result = p.parse(string)

        assert result == expected

    def test_object_in_object(self):
        p = parser.Parser()
        string = '{"parent": {"children": {"John": "male"}}}'
        expected = {"parent": {"children": {"John": "male"}}}

        result = p.parse(string)

        assert result == expected

    def test_object_in_array(self):
        p = parser.Parser()
        string = '[{"message": "HelloWorld", "theAnswer": 42}, 10000]'
        expected = [{"message": "HelloWorld", "theAnswer": 42}, 10000]

        result = p.parse(string)

        assert result == expected

    def test_objects_in_array(self):
        p = parser.Parser()
        string = """
        [
          {
            "message": "HelloWorld",
            "theAnswer": 42
          }
          ,
          {
            "message": "Goodbye,Space",
            "address": {
              "zipnumber": "1002000",
              "addr1": "XXX",
              "addr2": "YYY"
            }
          }
        ]
        """
        expected = [
            {"message": "HelloWorld", "theAnswer": 42},
            {
                "message": "Goodbye,Space",
                "address": {"zipnumber": "1002000", "addr1": "XXX", "addr2": "YYY"},
            },
        ]

        result = p.parse(string)

        assert result == expected

    def test_object_empty_key(self):
        p = parser.Parser()
        string = '{"": 10}'
        expected = {"": 10}

        result = p.parse(string)
        assert result == expected

    def test_complex_text(self):
        p = parser.Parser()
        string = dedent(
            """\
        [
          {
            "precision": "zip",
            "Latitude":  37.7668,
            "Longitude": -122.3959,
            "Address":   "",
            "City":      "SAN FRANCISCO",
            "State":     "CA",
            "Zip":       "94107",
            "Country":   "US"
          },
          {
            "precision": "zip",
            "Latitude":  37.371991,
            "Longitude": -122.026020,
            "Address":   "",
            "City":      "SUNNYVALE",
            "State":     "CA",
            "Zip":       "94085",
            "Country":   "US"
          }
        ]
        """
        )
        expected = [
            {
                "precision": "zip",
                "Latitude": 37.7668,
                "Longitude": -122.3959,
                "Address": "",
                "City": "SAN FRANCISCO",
                "State": "CA",
                "Zip": "94107",
                "Country": "US",
            },
            {
                "precision": "zip",
                "Latitude": 37.371991,
                "Longitude": -122.026020,
                "Address": "",
                "City": "SUNNYVALE",
                "State": "CA",
                "Zip": "94085",
                "Country": "US",
            },
        ]

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
        string = '''"
        "'''
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
        string = "[2.]"
        with pytest.raises(ValueError):
            p.parse(string)

        p = parser.Parser()
        string = "{1:"
        with pytest.raises(ValueError):
            p.parse(string)

    def test_trailing_comma(self):
        p = parser.Parser()
        string = "[1,]"
        with pytest.raises(ValueError):
            p.parse(string)

        string = '{"x": 123,}'
        with pytest.raises(ValueError):
            p.parse(string)
