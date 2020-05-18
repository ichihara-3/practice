import asyncio
import pprint
import tracemalloc

tracemalloc.start()

async def nested():
    return 42

async def parent():
    # coroutine objectが作られるがawaitされないため
    # 実行されない
    nested()

    # coroutine object が実行される
    print(await nested())

async def main():

    await parent()


asyncio.run(main())


snapshot = tracemalloc.take_snapshot()

pprint.pprint(snapshot.statistics('lineno'))
