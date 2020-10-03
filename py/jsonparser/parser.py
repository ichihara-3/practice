class WS:

    values = ("\x20", "\x09", "\x0a", "\x0d")


class Parser:
    def parse(self, string):
        string = self._trim_ws(string)
        if string == "null":
            return None
        if string == "true":
            return True
        if string == "false":
            return False
        if string[0] == "[":
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
        if string[0] == '"':
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
                if escaped:
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
                    if s == 'u':
                        unicode_char = True
                        unicode_line += '\\u'
                        continue
                if unicode_char:
                    unicode_line += s
                    if len(unicode_line) == 6:
                        char = eval('"{}"'.format(unicode_line))
                        line += char
                        unicode_line = ''
                        unicode_char = False
                        escaped = False
                    continue
                line += s
            return str(line)
        if "." in string:
            return float(string)
        return int(string)

    def _trim_ws(self, string):
        return string.strip("".join(WS.values))
