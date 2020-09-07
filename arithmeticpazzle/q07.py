import datetime

def main():
    fr = datetime.date(1964, 10, 10)
    to = datetime.date(2020, 7, 24)
    now = fr
    answers = []
    while now < to:
        strnow = now.strftime('%Y%m%d')
        binnow = bin(int(strnow, base=10))[2:]
        reverseint = int(''.join(reversed(binnow)), base=2)

        if strnow == str(reverseint):
            answers.append(strnow)

        now += datetime.timedelta(days=1)
    print('\n'.join(answers))


if __name__ == '__main__':
    main()
