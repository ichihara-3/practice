import re


class WS:

    values = ("\x20", "\x09", "\x0a", "\x0d")


class Number:
    pattern = re.compile(r'^-?(0|[1-9]\d*)(\.\d+)?([eE]\d+)?$', re.ASCII)


def is_null(string):
    return string == "null"


def is_true(string):
    return string == "true"


def is_false(string):
    return string == "false"


def is_string(string):
    return string.startswith('"') and string.endswith('"')


def is_array(string):
    return string.startswith('[') and string.endswith(']')


def is_object(string):
    return string.startswith('{') and string.endswith('}')


def is_number(string):
    if Number.pattern.match(string) is None:
        return False
    return True



def is_float(string):
    if not is_number(string):
        return False
    return '.' in string or 'e' in string or 'E' in string


def is_int(string):
    return is_number(string) and not is_float(string)


class Parser:
    def parse(self, string):
        string = self._trim_ws(string)
        if is_null(string):
            return None
        if is_true(string):
            return True
        if is_false(string):
            return False
        if is_array(string):
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
        if is_object(string):
            return dict()
        if is_string(string):
            line = ""
            escaped = False
            unicode_char = False
            unicode_line = ""
            for s in string[1:]:
                if s == '\\' and not escaped:
                    escaped = True
                    continue
                if s == '"' and not escaped:
                    break
                if escaped and not unicode_char:
                    escape_map = {
                        '"': '\"',
                        '\\': '\\',
                        '/': '/',
                        'b': '\b',
                        'f': '\f',
                        'n': '\n',
                        'r': '\r',
                        't': '\t',
                    }
                    if s in escape_map:
                        line += escape_map[s]
                        escaped = False
                        continue
                    elif s == 'u':
                        unicode_char = True
                        unicode_line += '\\u'
                        continue
                    else:
                        raise ValueError('non supported escape sequence: {}'.format(string))
                if unicode_char:
                    ordinal = ord(s)
                    if 48 <= ordinal <= 57 or 65 <= ordinal <= 70 or 97 <= ordinal<=102:
                        unicode_line += s
                    else:
                        raise ValueError('unexpected character while processing escape: {}'.format(string))
                    if len(unicode_line) == 6:
                        char = eval('"{}"'.format(unicode_line))
                        line += char
                        unicode_line = ''
                        unicode_char = False
                        escaped = False
                    continue
                line += s
            else:
                raise ValueError('unexpected end of line while scanning: {}'.format(string))
            if escaped:
                raise ValueError('unexpected end of line while processing escape: {}'.format(string))
            return str(line)
        if is_number(string):
            if is_float(string):
                return float(string)
            else:
                return int(string)
        else:
            raise ValueError('invalid object literal: {}'.format(string))


    def _trim_ws(self, string):
        return string.strip("".join(WS.values))
