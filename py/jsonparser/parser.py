

class Parser:

    def parse(self, string):
        if string == 'null':
            return None
        if string[0] == '[':
            contents = []
            element = ''
            for s in string[1:]:
                if s == ']':
                    if element:
                        contents.append(element)
                    break
                if s == ',':
                    contents.append(element)
                    element = ''
                    continue
                element += s
            return list(map(self.parse, contents))
        if string[0] == '"':
            return str(string[1:-1])
        if '.' in string:
            return float(string)
        return int(string)
