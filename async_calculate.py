import asyncio, time


async def power_of_ten(num):
    # print(f"Start processing {num}.")
    res = await num**10
    # print(f"The result of {num} is {res}.")
    return res


async def main():
    tasks = [
        asyncio.create_task(power_of_ten(i)) for i in range(114514, 191981)
    ]
    await asyncio.wait(tasks)
    print(sum(tasks))


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f'{time.time()-start} seconds used.')
