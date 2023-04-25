"""Brainfuck implemented in Python

Example:
    $ python3 brainfuck.py
    ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
    Hello, World!
"""

import sys

DEBUG=False

class Tokens:

    def __init__(self, tokens: list[str], debug = False):
        self._tokens = tokens
        self._debug = debug

    def __len__(self):
        return len(self._tokens)

    def get(self, pos):
        if pos > len(self._tokens):
            raise ValueError("the position is out of range")
        if self._debug:
            print(f"{pos=}, token={self._tokens[pos]}")
        return self._tokens[pos]

def tokenize(program: str) -> Tokens:
    return Tokens(list(program), debug=DEBUG)


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename) as f:
            program = f.read()
    else:
        program = input()

    ptr = 0
    code_pos = 0
    mem = [0]*30000
    stack = []
    depth = 0
    code = tokenize(program)

    while code_pos < len(code):
        token_ = code.get(code_pos)
        if token_ == "+":
            mem[ptr] += 1
        elif token_ == "-":
            mem[ptr] -= 1
        elif token_ == ">":
            ptr += 1
        elif token_ == "<":
            ptr -= 1
        elif token_ == ".":
            print(chr(mem[ptr]), end='')
        elif token_ == ",":
            mem[ptr] == ord(input())
        elif token_ == "[":
            if mem[ptr] == 0:
                depth += 1
                while depth >= 1:
                    code_pos += 1
                    if code_pos > len(code):
                        raise ValueError('EOL found while searching for `]`')
                    token_ = code.get(code_pos)
                    if token_ == "]":
                        depth -= 1
                    elif token_ == "[":
                        depth += 1
            else:
                stack.append(code_pos)
        elif token_ == "]":
            if mem[ptr] == 0:
                stack.pop()
            else:
                code_pos = stack[-1]
        code_pos += 1


if __name__ == "__main__":
    main()