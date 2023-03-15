import random
import string

def caesar(s, shift):
    result = ''
    for c in s:
        if c in string.ascii_uppercase:
            result += chr((ord(c) + (shift%26) - ord('A'))%26 + ord('A'))
        elif c in string.ascii_lowercase:
            result += chr((ord(c) + (shift%26) - ord('a'))%26 + ord('a'))
        else:
            result += c
    return result


if __name__ == '__main__':
    shift = random.randint(1, 25)
    print(shift)
    while True:
        s = input('Enter a string: ')
        print(caesar(s, shift))