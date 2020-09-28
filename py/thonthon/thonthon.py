import sys
import traceback


def main():
    sys.exit(repl())


def repl():
    gn = {}
    ln = {}

    while True:
        try:
            lines = read()
            result = execute(lines, gn, ln)
        except KeyboardInterrupt:
            print('Good bye...')
            return 0
        except Exception:
            traceback.print_exc(file=sys.stdout)


def read(prompt1=None, prompt2=None):
    if prompt1 is None:
        prompt1 = 'thonthon> '
    if prompt2 is None:
        prompt2 = '... '
    in_lines = False

    lines = []
    line = input(prompt1)
    lines.append(line)
    if lines[-1] == ':':
        in_lines = True
    while in_lines:
        line = input(prompt2)
        in_lines =False
    return '\n'.join(lines)
    



def execute(lines, globalnamespace, localnamespace):
    exec(lines, globalnamespace, localnamespace)


if __name__ == '__main__':
    main()