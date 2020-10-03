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
            for s in string[1:]:
                if s == '"':
                    break
                line += s
            return str(line)
        if "." in string:
            return float(string)
        return int(string)

    def _trim_ws(self, string):
        return string.strip("".join(WS.values))
