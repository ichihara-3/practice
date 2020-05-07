def hello():
    hello = yield "Hello"
    yield hello

h = hello()

print(next(h))

print(h.send("World"))
