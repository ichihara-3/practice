import asyncio
import time


async def hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")


asyncio.run(hello())


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(2, "world"))

    print(f"started at {time.strftime('%X')}")

    await task2
    await task1

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
