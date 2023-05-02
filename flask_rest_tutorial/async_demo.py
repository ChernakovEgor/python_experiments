import asyncio
from time import sleep

async def fetch_data():
    print('Start fetching')
    await asyncio.sleep(2)
    # sleep(2)
    print('Fetching is done')
    return 'data'

async def numbers():
    for i in range(0, 10):
        await asyncio.sleep(0.25)
        # sleep(0.25)
        print(i)

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = asyncio.create_task(fetch_data())
        task2 = asyncio.create_task(numbers())
    
    value = task1.result()
    print(value)

asyncio.run(main())
