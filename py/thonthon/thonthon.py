#!/usr/bin/env python3
u"""Simple Python REPL implemented in python3
"""
import copy
import readline
import rlcompleter
import sys
import traceback

__version__ = "0.0.1"


readline.parse_and_bind("tab: complete")


def repl():
    gn = {}
    ln = {}
    while True:
        try:
            lines = read()
            if not lines:
                continue
            result = evaluate(lines, gn, ln)
            print(result)
        except (KeyboardInterrupt, EOFError):
            print("Good bye...")
            return 0
        except (SystemExit) as e:
            print("Good bye...")
            return e.code
        except NoOutput:
            pass
        except Exception:
            traceback.print_exc(file=sys.stdout)


def read(prompt1=None, prompt2=None):
    if prompt1 is None:
        prompt1 = "thonthon> "
    if prompt2 is None:
        prompt2 = "...     > "
    in_lines = False

    lines = []
    line = input(prompt1)
    if not line:
        return ""
    lines.append(line)
    if line[-1] in (":", "\\") or _in_brackets(line):
        in_lines = True
    while in_lines:
        line = input(prompt2)
        if line.strip().replace("\t", "").replace(" ", "") == "":
            in_lines = False
        lines.append(line)
    return "\n".join(lines)


def _in_brackets(line):
    brackets = (
        ("(", ")"),
        ("[", "]"),
        ("{", "}"),
    )
    for start, end in brackets:
        if start in line and end not in line:
            return True
    else:
        return False


def evaluate(lines, globalnamespace, localnamespace):
    try:
        result = eval(lines, globalnamespace, localnamespace)
        return result
    except SyntaxError:
        exec(lines, globalnamespace, localnamespace)
        raise NoOutput


class NoOutput(Exception):
    pass


def main():
    sys.exit(repl())


if __name__ == "__main__":
    import sys

    print("thonthon {ver}".format(ver=__version__))
    print("python version: {pyver}".format(pyver=sys.version))
    main()
