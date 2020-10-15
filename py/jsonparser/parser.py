import re


class WS:

    values = (
        "\x20",  # スペース
        "\x09",  # 平行タブ
        "\x0a",  # 改行または埋め込み改行(LF)
        "\x0d",  # 復帰改行(CR)
    )


class StructualChars:

    begin_array = "\x5b"  # 左角括弧 [
    begin_object = "\x7b"  # 左中括弧 {
    end_array = "\x5d"  # 右角括弧 ]
    end_object = "\x7d"  # 右中括弧 ]
    name_separator = "\x3a"  # コロン   :
    value_separator = "\x2c"  # コンマ   ,


class Number:
    pattern = re.compile(r"(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?", re.ASCII)


class String:
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
    controll_chars = (
        "\x00",
        "\x01",
        "\x02",
        "\x03",
        "\x04",
        "\x05",
        "\x06",
        "\x07",
        "\x08",
        "\x09",
        "\x0a",
        "\x0b",
        "\x0c",
        "\x0d",
        "\x0e",
        "\x0f",
        "\x10",
        "\x11",
        "\x12",
        "\x13",
        "\x14",
        "\x15",
        "\x16",
        "\x17",
        "\x18",
        "\x19",
        "\x1a",
        "\x1b",
        "\x1c",
        "\x1d",
        "\x1e",
        "\x1f",
    )
    chunk = re.compile(r'(.*?)(["\\\x00-\x1f])')
    escape = "\\"
    unicode_char = "u"
    quotation_mark = '"'


def is_number(string):
    m = Number.pattern.match(string)
    if m is None:
        return False
    if string[m.end():]:
        return False
    return True


def trim_ws(string):
    return string.strip("".join(WS.values))


def is_float(string):
    if not is_number(string):
        return False
    return "." in string or "e" in string or "E" in string


class Parser:

    def parse(self, string):
        res, pos = self._parse(string)
        if len(trim_ws(string[pos:])):
            raise ValueError('unexpected trailing characters: {}'.format(string[pos:]))
        return res

    def _parse(self, string, pos=0):
        while pos < len(string):
            char = string[pos]
            if char in WS.values:
                pos += 1
            else:
                break
        char = string[pos]
        if char == 'n' and string[pos:pos+len('null')] == 'null':
            pos += len('null')
            return None, pos
        if char == 't' and string[pos:pos+len('true')] == 'true':
            pos += len('true')
            return True, pos
        if char == 'f' and string[pos:pos+len('false')] == 'false':
            pos += len('false')
            return False, pos
        if char == '"':
            result, pos =  self._parse_string(string, pos)
            return result, pos
        if char == '[':
            result, pos = self._parse_array(string, pos)
            return result, pos
        if char == '{':
            result, pos = self._parse_object(string, pos)
            return result, pos
        result, pos = self._parse_number(string, pos)
        return result, pos

    def _parse_number(self, string, pos):
        m = Number.pattern.match(string[pos:])
        if not m:
            raise ValueError('not a number')
        num = m.group(0)
        pos += m.end()
        if is_float(num):
            return float(num), pos
        else:
            return int(num), pos

    def _parse_object(self, string, pos):
        if string[pos] != StructualChars.begin_object:
            raise ValueError('not an object')
        pos += 1
        result = {}
        has_next = False
        while string[pos] != StructualChars.end_object:
            has_key = False
            has_next = False
            # scan key
            while not has_key:
                s = string[pos]
                if s in WS.values:
                    pos += 1
                    continue
                elif s == String.quotation_mark:
                    key, pos = self._parse_string(string, pos)
                    has_key = True
                else:
                    raise ValueError("unexpected Token")
            while string[pos] != StructualChars.name_separator:
                pos += 1
            pos += 1
            # scan value
            value, pos = self._parse(string, pos)
            result[key] = value
            while string[pos] != StructualChars.value_separator and string[pos] != StructualChars.end_object:
                if string[pos] not in WS.values:
                    raise ValueError('unexpected token {}: expected ,'.format(string[pos]))
                pos += 1
            if string[pos] == StructualChars.value_separator:
                pos += 1
                has_next = True
        if has_next:
            raise ValueError('unexpected comma')
        pos += 1
        return result, pos

    def _parse_array(self, string, pos):
        if string[pos] != StructualChars.begin_array:
            raise ValueError('not an object')
        pos += 1
        items = []
        has_next = False
        while string[pos] != StructualChars.end_array:
            has_next = False
            item, pos = self._parse(string, pos)
            items.append(item)
            while string[pos] != StructualChars.value_separator and string[pos] != StructualChars.end_array:
                if string[pos] not in WS.values:
                    raise ValueError('unexpected token {}: expected ,'.format(string[pos]))
                pos += 1
            if pos >= len(string):
                raise ValueError('unexpected end of the text')
            if string[pos] == StructualChars.value_separator:
                pos += 1
                has_next = True
            if pos >= len(string):
                raise ValueError('unexpected end of the text')
        if has_next:
            raise ValueError("trailing comma found")
        pos += 1
        return items, pos

    def _parse_string(self, string, pos):
        if string[pos] != String.quotation_mark:
            raise ValueError('not a string')
        pos += 1
        line = ""
        unicode_line = ""
        while True:
            m = String.chunk.match(string[pos:])
            if m is None:
                raise ValueError('unterminated string')
            data, s = m.groups()
            line += data
            pos += m.end()
            if s == String.quotation_mark:
                break
            if pos >= len(string):
                raise ValueError('EOF while scanning string')
            if s in String.controll_chars:
                raise ValueError(
                    "controll chars not allowed to place in the string:{}".format(
                        repr(s)
                    )
                )
            if s == String.escape:
                s = string[pos]
                if s in String.escape_map:
                    line += String.escape_map[s]
                    pos +=1
                    continue
                elif s == String.unicode_char:
                    unicode_line += "\\u"
                    pos +=1
                else:
                    raise ValueError("non supported escape sequence: {}".format(string))
                if unicode_line:
                    hexes = string[pos:pos+4]
                    if len(hexes) < 4:
                        raise ValueError("non supported unicode line")
                    pos += 4
                    for s in hexes:
                        ordinal = ord(s)
                        if 48 <= ordinal <= 57 or 65 <= ordinal <= 70 or 97 <= ordinal <= 102:
                            unicode_line += s
                        else:
                            raise ValueError(
                                "unexpected character while processing escape: {}".format(
                                    string
                                )
                            )
                    char = eval('"{}"'.format(unicode_line))
                    line += char
                    unicode_line = ""
                    continue
        return line, pos


if __name__ == "__main__":
    import sys

    p = Parser()
    result = p.parse(sys.stdin.read())

    def print_with_type(obj, indent=0):
        if isinstance(obj, dict):
            print("{indent}{{".format(indent="  " * indent))
            for k, v in obj.items():
                print(
                    "{indent}{k}:{tk}:".format(
                        indent="  " * (indent + 1), k=repr(k), tk=type(k)
                    )
                )
                print_with_type(v, indent + 2)
            print("{indent}}}".format(indent="  " * indent))
        elif isinstance(obj, list):
            print("{indent}[".format(indent="  " * indent))
            for v in obj:
                print_with_type(v, indent + 1)
            print("{indent}]".format(indent="  " * indent))
        else:
            print(
                "{indent}{obj}:{to}".format(
                    indent="  " * indent, obj=repr(obj), to=type(obj)
                )
            )

    print_with_type(result)
