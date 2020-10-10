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
    pattern = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?([eE][-+]?\d+)?$", re.ASCII)


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
    escape = "\\"
    unicode_char = "u"
    quotation_mark = '"'


def is_ws(char):
    return char in Ws.values


def is_null(string):
    return string == "null"


def is_true(string):
    return string == "true"


def is_false(string):
    return string == "false"


def is_string(string):
    return string.startswith(String.quotation_mark) and string.endswith(
        String.quotation_mark
    )


def is_array(string):
    return string.startswith(StructualChars.begin_array) and string.endswith(
        StructualChars.end_array
    )


def is_object(string):
    return string.startswith(StructualChars.begin_object) and string.endswith(
        StructualChars.end_object
    )


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
            return self._to_object(string)
        if is_string(string):
            return self._to_string(string)
        if is_number(string):
            if is_float(string):
                return float(string)
            else:
                return int(string)
        else:
            raise ValueError("invalid object literal: {}".format(string))

    def _to_object(self, string):
        result = {}
        line = trim_ws(string[1:-1])
        if line == "":
            return result
        while len(line):
            in_key = False
            key = ""
            # scan key
            for i, s in enumerate(line):
                if s in WS.values and not in_key:
                    continue
                if s == String.quotation_mark:
                    if not in_key:
                        in_key = True
                    else:
                        if i > 0 and line[i - 1] != String.escape:
                            key += s
                            in_key = False
                            break
                if in_key:
                    key += s
                else:
                    raise ValueError("unexpected Token")
            line = line[i + 1 :]
            for i, s in enumerate(line):
                if s == StructualChars.name_separator:
                    break
            line = line[i + 1 :]
            # scan value
            value = ""
            obj_depth = 0
            array_depth = 0
            in_str = False
            for j, s in enumerate(line):
                if s == String.quotation_mark:
                    if not in_str:
                        in_str = True
                    elif in_str and line[j - 1] != String.escape:
                        in_str = False
                if s == StructualChars.begin_array:
                    if not in_str:
                        array_depth += 1
                if s == StructualChars.end_array:
                    if not in_str:
                        array_depth -= 1
                        if array_depth < 0:
                            raise ValueError("invalid syntax: {}".format(string))
                if s == StructualChars.begin_object:
                    if not in_str:
                        obj_depth += 1
                if s == StructualChars.end_object:
                    if not in_str:
                        obj_depth -= 1
                        if obj_depth < 0:
                            raise ValueError("invalid syntax: {}".format(string))
                if s == StructualChars.value_separator:
                    if not in_str and array_depth == 0 and obj_depth == 0:
                        break
                value += s
            result[self._to_string(key)] = self.parse(value)
            line = line[j + 1 :]
        return result

    def _to_array(self, string):
        items = []
        content = trim_ws(string[1:-1])
        while len(content):
            item = ""
            array_depth = 0
            obj_depth = 0
            in_str = False
            for i, s in enumerate(content):
                if s == String.quotation_mark:
                    if not in_str:
                        in_str = True
                    elif in_str and content[i - 1] != String.escape:
                        in_str = False
                if s == StructualChars.begin_array:
                    if not in_str:
                        array_depth += 1
                if s == StructualChars.end_array:
                    if not in_str:
                        array_depth -= 1
                        if array_depth < 0:
                            raise ValueError("invalid syntax: {}".format(string))
                if s == StructualChars.begin_object:
                    if not in_str:
                        obj_depth += 1
                if s == StructualChars.end_object:
                    if not in_str:
                        obj_depth -= 1
                        if obj_depth < 0:
                            raise ValueError("invalid syntax: {}".format(string))
                if s == StructualChars.value_separator:
                    if not in_str and array_depth == 0 and obj_depth == 0:
                        break
                item += s
            items.append(item)
            content = content[i + 1 :]
        return list(map(self.parse, items))

    def _to_string(self, string):
        string = trim_ws(string)
        line = ""
        escaped = False
        unicode_char = False
        unicode_line = ""
        for s in string[1:]:
            if s == String.escape and not escaped:
                escaped = True
                continue
            if s == String.quotation_mark and not escaped:
                break
            if escaped and not unicode_char:
                if s in String.escape_map:
                    line += String.escape_map[s]
                    escaped = False
                    continue
                elif s == String.unicode_char:
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
