import re


class WS:

    values = ("\x20", "\x09", "\x0a", "\x0d")


class Value:
    pass


class Null(Value):
    pass


class PyTrue(Value):
    pass


class PyFalse(Value):
    pass


class Number(Value):
    pattern = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?([eE]\d+)?$", re.ASCII)

    def __init__(self, line):
        self._line = line


class Float(Number):
    pass


class Int(Number):
    pass


class String(Value):
    escape_map = {
        '"': '"',
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }
    unicode_char = "u"

    def __init__(self, line):
        self._line = line


class Array(Value):

    def __init__(self, line):
        self._line = line
        self._contents = []
        self._tokenize(line)

    def _tokenize(self):
        string = ""
        escaped = False
        for s in self._line:
            if s == "\\" and not escaped:
                escaped = True
            if s == "," and escaped:
                self._contents.append(tokeninze(s))
            string+=s
            if escaped:
                escaped = False


class Object(Value):

    def __init__(self, line):
        self._line = line
        self._contents = []


    def _tokenize(self):
        string = ""
        escaped = False
        for s in self._line:
            if s == "\\" and not escaped:
                escaped = True
            if s == "," and escaped:
                self._contents.append(tokeninze(s))
            string+=s
            if escaped:
                escaped = False


# Object(str).to_py_object()
# -> Object(Key:Str, Value:Object(...), Key: Str(xxx))

def tokeninze(string):
    string = trim_ws(string)
    if is_null(string):
        return Null()
    if is_true(string):
        return PyTrue()
    if is_false(string):
        return PyFalse()
    if is_array(string):
        return Array(string[1:-1])
    if is_object(string):
        return Object(string[1:-1])
    if is_string(string):
        return String(string[1:-1])
    if is_number(string):
        if is_float(string):
            return Float(string)
        else:
            return Int(string)
    else:
        raise ValueError("invalid object literal: {}".format(string))


def is_ws(char):
    return char in Ws.values


def is_null(string):
    return string == "null"


def is_true(string):
    return string == "true"


def is_false(string):
    return string == "false"


def is_string(string):
    return string.startswith('"') and string.endswith('"')


def is_array(string):
    return string.startswith("[") and string.endswith("]")


def is_object(string):
    return string.startswith("{") and string.endswith("}")


def is_number(string):
    if Number.pattern.match(string) is None:
        return False
    return True


def trim_ws(string):
    return string.strip("".join(WS.values))


def is_float(string):
    if not is_number(string):
        return False
    return "." in string or "e" in string or "E" in string


def is_int(string):
    return is_number(string) and not is_float(string)


class Parser:
    def parse(self, string):
        string = trim_ws(string)
        if is_null(string):
            return None
        if is_true(string):
            return True
        if is_false(string):
            return False
        if is_array(string):
            return self._to_array(string)
        if is_object(string):
            result = {}
            content = trim_ws(string[1:-1])
            if content == "":
                return result
            elements = content.split(",")
            for e in elements:
                k, v = e.split(":")
                result[self._to_string(k)] = self.parse(v)
            return result
        if is_string(string):
            return self._to_string(string)
        if is_number(string):
            if is_float(string):
                return float(string)
            else:
                return int(string)
        else:
            raise ValueError("invalid object literal: {}".format(string))


    def _to_array(self, string):
        string = trim_ws(string)
        contents = []
        element = ""
        depth = 1
        for s in string[1:]:
            if s == "[":
                depth += 1
            if s == "]":
                depth -= 1
                if depth == 0:
                    if element:
                        contents.append(element)
                    break
            if s == "," and depth == 1:
                contents.append(element)
                element = ""
                continue
            element += s
        return list(map(self.parse, contents))

    def _to_string(self, string):
        string = trim_ws(string)
        line = ""
        escaped = False
        unicode_char = False
        unicode_line = ""
        for s in string[1:]:
            if s == "\\" and not escaped:
                escaped = True
                continue
            if s == '"' and not escaped:
                break
            if escaped and not unicode_char:
                if s in String.escape_map:
                    line += String.escape_map[s]
                    escaped = False
                    continue
                elif s == "u":
                    unicode_char = True
                    unicode_line += "\\u"
                    continue
                else:
                    raise ValueError("non supported escape sequence: {}".format(string))
            if unicode_char:
                ordinal = ord(s)
                if 48 <= ordinal <= 57 or 65 <= ordinal <= 70 or 97 <= ordinal <= 102:
                    unicode_line += s
                else:
                    raise ValueError(
                        "unexpected character while processing escape: {}".format(
                            string
                        )
                    )
                if len(unicode_line) == 6:
                    char = eval('"{}"'.format(unicode_line))
                    line += char
                    unicode_line = ""
                    unicode_char = False
                    escaped = False
                continue
            line += s
        else:
            raise ValueError("unexpected end of line while scanning: {}".format(string))
        if escaped:
            raise ValueError(
                "unexpected end of line while processing escape: {}".format(string)
            )
        return line


if __name__ == '__main__':
    import sys
    p = Parser()
    print(p.parse(sys.stdin.read()))
