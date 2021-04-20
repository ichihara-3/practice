"""Json Parser

"""
# http://www.crockford.com/mckeeman.html
# This is the JSON grammar in McKeeman Form.
#
# json
#     element
#
# value
#     object
#     array
#     string
#     number
#     "true"
#     "false"
#     "null"
#
# object
#     '{' ws '}'
#     '{' members '}'
#
# members
#     member
# member ',' members
#
# member
#     ws string ws ':' element
#
# array
#     '[' ws ']'
#     '[' elements ']'
#
# elements
#     element
#     element ',' elements
#
# element
#     ws value ws
#
# string
#     '"' characters '"'
#
# characters
#     ""
#     character characters
#
# character
#     '0020' . '10FFFF' - '"' - '\'
#     '\' escape
#
# escape
#     '"'
#     '\'
#     '/'
#     'b'
#     'f'
#     'n'
#     'r'
#     't'
#     'u' hex hex hex hex
#
# hex
#     digit
#     'A' . 'F'
#     'a' . 'f'
#
# number
#     integer fraction exponent
#
# integer
#     digit
#     onenine digits
#     '-' digit
#     '-' onenine digits
#
# digits
#     digit
#     digit digits
#
# digit
#     '0'
#     onenine
#
# onenine
#     '1' . '9'
#
# fraction
#     ""
#     '.' digits
#
# exponent
#     ""
#     'E' sign digits
#     'e' sign digits
#
# sign
#     ""
#     '+'
#     '-'
#
# ws
#     ""
#     '0020' ws
#     '000A' ws
#     '000D' ws
#     '0009' ws

from enum import Enum
from enum import auto
from typing import List, Tuple, Any, NoReturn
import re


class TokenType(Enum):
    Reserved = auto()
    Number = auto()
    String = auto()
    TrueType = auto()
    FalseType = auto()
    Null = auto()


class NodeType(Enum):
    Object = auto()
    Array = auto()
    String = auto()
    Number = auto()
    TrueType = auto()
    FalseType = auto()
    Null = auto()


class Token:
    def __init__(self, t: TokenType, v: str = None, d: bool = None):
        self._type = t
        self._value = v
        self._is_decimal = d

    @property
    def type(self) -> Any:
        return self._type

    @property
    def value(self) -> Any:
        return self._value

    @property
    def is_decimal(self):
        return self._is_decimal


class Tokens:
    def __init__(self):
        self._tokens = []

    def __bool__(self):
        return bool(self._tokens)

    def push(self, o: Token) -> NoReturn:
        if not isinstance(o, Token):
            raise ValueError("expected Token class")
        self._tokens.append(o)

    def pop(self) -> Token:
        return self._tokens.pop(0)

    def is_empty(self):
        return len(self._tokens) == 0

    def consume(self, t: TokenType) -> Token:
        if self.is_empty():
            raise ValueError("No token exist")
        token = self._tokens[0]
        if token.type == t:
            return self.pop()
        return None

    def consume_reserved(self, string: str):
        token = self._tokens[0]
        if token.type == TokenType.Reserved and token.value == string:
            return self.pop()
        return None

    def consume_number(self):
        return self.consume(TokenType.Number)

    def consume_string(self):
        return self.consume(TokenType.String)

    def expect_type_of(self, t: TokenType):
        if self.is_empty():
            raise ValueError("No token exist")
        token = self._tokens[0]
        if token.type != t:
            raise ValueError("unexpected token")
        self._tokens.pop()

    def expect(self, string: str):
        token = self._tokens[0]
        if token and token.value == string:
            return self.pop()
        raise ValueError("expected %s" % string)


WS = ("\x20", "\x0a", "\x0d", "\x09")


def is_ws(char: str):
    return char in WS


def at_end_of_word(char: str):
    return is_ws(char) or char in (",", "]", "}")


ESCAPE = {
    '"': '"',
    "\\": "\\",
    "/": "/",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "u": "unicode",
}

ESCAPE_JSON = {
    '"': '\\"',
    "\\": "\\\\",
    "/": "\\/",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}


CONTROL_CHARS = [chr(x) for x in range(0, 32)]


UNICODE = re.compile("^[0-9a-zA-Z]{4}", re.ASCII)


def get_escaped(char: str):
    return ESCAPE.get(char)


class Tokenizer:
    def tokenize(self, jsonstring: str) -> List[Token]:
        tokens = Tokens()
        length = len(jsonstring)
        i = 0
        while i < length:
            if is_ws(jsonstring[i]):
                i += 1
                continue
            elif jsonstring[i : i + 5] == "false" and (
                i + 5 == length or at_end_of_word(jsonstring[i + 5])
            ):
                tokens.push(Token(TokenType.FalseType))
                i += 5
                continue
            elif jsonstring[i : i + 4] == "true" and (
                i + 4 == length or at_end_of_word(jsonstring[i + 4])
            ):
                tokens.push(Token(TokenType.TrueType))
                i += 4
                continue
            elif jsonstring[i : i + 4] == "null" and (
                i + 4 == length or at_end_of_word(jsonstring[i + 4])
            ):
                tokens.push(Token(TokenType.Null))
                i += 4
                continue
            elif jsonstring[i] == '"':
                i += 1
                string = ""
                escaped = False
                closed = False
                j = 0
                while i + j < length:
                    if escaped:
                        key = jsonstring[i + j]
                        char = get_escaped(key)
                        if not char:
                            raise ValueError("invalid escape char %s" % key)
                        if char == "unicode":
                            m = UNICODE.match(jsonstring[i + j + 1 : i + j + 5])
                            if not m:
                                raise ValueError("invalid unicode literal")
                            string += chr(int(m.group(0), 16))
                            j += 5
                        else:
                            string += char
                            j += 1
                        escaped = False
                        continue
                    if jsonstring[i + j] == '"':
                        closed = True
                        j += 1
                        break
                    if jsonstring[i + j] == "\\":
                        escaped = True
                        j += 1
                        continue
                    if ord(jsonstring[i + j]) < 20:
                        raise ValueError("invalid character")
                    string += jsonstring[i + j]
                    j += 1
                if not closed:
                    raise ValueError("unexpected EOL while searching for '\"'")
                tokens.push(Token(TokenType.String, v=string))
                i += j
                continue
            elif jsonstring[i] in "[]{},:":
                tokens.push(Token(TokenType.Reserved, jsonstring[i]))
                i += 1
                continue

            else:
                offset, is_decimal = parse_number(jsonstring, i)
                tokens.push(
                    Token(TokenType.Number, jsonstring[i : i + offset], d=is_decimal)
                )
                i += offset
                continue
        return tokens


def parse_integer(jsonstring: str, i: int) -> int:
    char = jsonstring[i]
    offset = 1
    if char == "-":
        if i + offset >= len(jsonstring):
            raise ValueError("unexpected EOL")
        char = jsonstring[i + offset]
        offset += 1
    if char == "0":
        return offset
    elif is_onenine(char):
        while i + offset < len(jsonstring) and is_digit(jsonstring[i + offset]):
            offset += 1
        return offset
    else:
        raise ValueError("not an integer")


def parse_fraction(jsonstring: str, i: int) -> int:
    offset = 0
    if jsonstring[i] != ".":
        return offset
    offset += 1
    if i + offset >= len(jsonstring) or not is_digit(jsonstring[i + offset]):
        raise ValueError("not a fraction")
    while i + offset < len(jsonstring) and is_digit(jsonstring[i + offset]):
        offset += 1
    return offset


def parse_exponent(jsonstring: str, i: int) -> int:
    offset = 0
    if jsonstring[i] not in "eE":
        return offset
    offset += 1
    if i + offset >= len(jsonstring):
        raise ValueError("exponent expressions are expected")
    if jsonstring[i + offset] in "+-":
        offset += 1
    if i + offset >= len(jsonstring) or not is_digit(jsonstring[i + offset]):
        raise ValueError("exponent expressions are expected")
    while is_digit(jsonstring[i + offset]):
        offset += 1
    return offset


def is_digit(char: str):
    return char in "0123456789"


def is_onenine(char: str):
    return char in "123456789"


def parse_number(string: str, start: int) -> Tuple[int, bool]:
    is_decimal = False
    offset = parse_integer(string, start)
    start += offset
    if start >= len(string):
        return offset, is_decimal
    f = parse_fraction(string, start)
    if f:
        is_decimal = True
        offset += f
        start += f
        if start >= len(string):
            return offset, is_decimal
    e = parse_exponent(string, start)
    if e:
        is_decimal = True
        offset += e
    return offset, is_decimal


class JsonObject:
    def __init__(self, v: str = None, d: bool = False, e=None, m=None):
        self._is_decimal = d
        self._value = str(v)
        self._elements = [] if e is None else e
        self._members = [] if m is None else m

    def to_py_object(self) -> Any:
        pass

    def to_string(self) -> str:
        pass


class Null(JsonObject):
    def to_py_object(self):
        return None

    def to_string(self):
        return "null"


class TrueObject(JsonObject):
    def to_py_object(self):
        return True

    def to_string(self):
        return "true"


class FalseObject(JsonObject):
    def to_py_object(self):
        return False

    def to_string(self):
        return "false"


class String(JsonObject):
    def to_py_object(self):
        return self._value

    def to_string(self):
        res = ""
        for c in self._value:
            if c in CONTROL_CHARS:
                res += "u" + hex(ord(c))[2:].zfill(4)
            elif c in ESCAPE_JSON:
                res += ESCAPE_JSON[c]
            else:
                res += c
        return f'"{res}"'


class Number(JsonObject):
    def to_py_object(self):
        if self._is_decimal:
            return float(self._value)
        else:
            return int(self._value)

    def to_string(self):
        return self._value


class Array(JsonObject):
    def to_py_object(self):
        return [e.to_py_object() for e in self._elements]

    def to_string(self):
        return "[" + ",".join(e.to_string() for e in self._elements) + "]"


class Object(JsonObject):
    def to_py_object(self):
        return {m.key: m.value.to_py_object() for m in self._members}

    def to_string(self):
        return (
            "{"
            + ",".join(
                String(m.key).to_string() + ":" + m.value.to_string()
                for m in self._members
            )
            + "}"
        )


class ObjMember:
    def __init__(self, k: str, v: JsonObject):
        self._key = k
        self._value = v

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> JsonObject:
        return self._value


class Parser:
    def parse(self, tokens: Tokens) -> JsonObject:
        return self._json(tokens)

    def _json(self, tokens: Tokens) -> JsonObject:
        return self._element(tokens)

    def _element(self, tokens: Tokens) -> JsonObject:
        return self._value(tokens)

    def _value(self, tokens: Tokens) -> JsonObject:
        if tokens.consume(TokenType.Null):
            return Null()
        if tokens.consume(TokenType.TrueType):
            return TrueObject()
        if tokens.consume(TokenType.FalseType):
            return FalseObject()
        if tokens.consume_reserved("["):
            return Array(e=self._array(tokens))
        if tokens.consume_reserved("{"):
            return Object(m=self._object(tokens))
        string = tokens.consume(TokenType.String)
        if string:
            return String(v=string.value)
        number = tokens.consume_number()
        if number:
            return Number(v=number.value, d=number.is_decimal)
        raise ValueError("unexpected token")

    def _object(self, tokens: Tokens) -> List[ObjMember]:
        ret = []
        while not tokens.consume_reserved("}"):
            if tokens.is_empty():
                raise ValueError("EOL while parsing object")
            if ret:
                tokens.expect(",")
            ret.append(self._obj_member(tokens))
        return ret

    def _obj_member(self, tokens: Tokens) -> ObjMember:
        key = tokens.consume_string()
        if not key:
            raise ValueError("key must be type of string")
        tokens.expect(":")
        return ObjMember(key.value, self._element(tokens))

    def _array(self, tokens: Tokens) -> List[JsonObject]:
        ret = []
        while not tokens.consume_reserved("]"):
            if tokens.is_empty():
                raise ValueError("EOL while parsing array")
            if ret:
                tokens.expect(",")
            ret.append(self._element(tokens))
        return ret


class Assignor:
    def assign(self, pythonobject) -> JsonObject:
        if pythonobject is None:
            return Null()
        if pythonobject is True:
            return TrueObject()
        if pythonobject is False:
            return FalseObject()
        if isinstance(pythonobject, str):
            return String(v=pythonobject)
        if isinstance(pythonobject, float):
            return Number(v=str(pythonobject), d=True)
        if isinstance(pythonobject, int):
            return Number(v=str(pythonobject), d=False)
        if isinstance(pythonobject, (list, tuple)):
            return Array(e=[self.assign(el) for el in pythonobject])
        if isinstance(pythonobject, dict):
            return Object(
                m=[
                    ObjMember(key, self.assign(value))
                    for key, value in pythonobject.items()
                ]
            )
        raise ValueError("could not assign to json element: %s" % pythonobject)


class Json:
    def serialize(self, pythonobject: Any):
        "Serialize python object to json"
        assignor = Assignor()
        json_object = assignor.assign(pythonobject)
        return json_object.to_string()

    def deserialize(self, jsonstring: str) -> Any:
        """Deseiralize s to a python object."""
        t = Tokenizer()
        p = Parser()
        tokens = t.tokenize(jsonstring)
        json_object = p.parse(tokens)
        return json_object.to_py_object()


if __name__ == "__main__":
    import sys

    j = Json()
    string = sys.stdin.read()
    pyobj = j.deserialize(string)
    print(pyobj)

    print(j.serialize(pyobj))
