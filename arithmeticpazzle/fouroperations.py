# プログラマ脳を鍛える数学パズル　第一章 Q02 数列の四則演算
from itertools import product
from typing import List
import re

PATTERN = re.compile(r'(?<=[^0-9])0([0-9]+)')

def solve(start: int, end: int) -> List[int]:
    answer = []
    for i in range(start, end+1):
        if calc_answer_is_reverse_of(i):
            answer.append(i)
    return answer

def calc_answer_is_reverse_of(i: int) -> bool:
    # operators = ['+', '-', '*', '/', '']
    operators = ['*', '']
    numbers = list(str(i))
    for op1, op2, op3 in product(operators, repeat=len(numbers)-1):
        if op1 == op2 == op3 == '':
            continue
        try:
            line = numbers[0] + op1 + numbers[1] + op2 + numbers[2] + op3 + numbers[3]
            while PATTERN.search(line):
                line = PATTERN.sub(r'\1', line)
            result = eval(line)
        except ZeroDivisionError:
            continue
        if str(result) == ''.join(reversed(str(i))):
            return True
    else:
        return False


def main():
    print(' '.join(map(str, solve(1000, 9999))))


if __name__ == '__main__':
    main()
