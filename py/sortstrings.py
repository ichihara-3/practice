import sys

def main():
    f = sys.stdin
    strings = []
    for l in f:
        strings.append(l.strip())
    print('\n'.join(sorted(strings)))


if __name__ == '__main__':
    main()
