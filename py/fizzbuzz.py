list(
    map(
        print,
        map(
            lambda x: "Fizz" if isinstance(x, int) and x % 3 == 0 else x,
            map(
                lambda x: "Buzz" if isinstance(x, int) and x % 5 == 0 else x,
                map(lambda x: "FizzBuzz" if x % 15 == 0 else x, range(1, 101)),
            ),
        ),
    )
)
