import asyncio, time
from client import main
from threading import Thread

request_num = 1000


def main_wrapped():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('User exit.')


if __name__ == '__main__':
    threads = [
        Thread(target=main_wrapped, args=()) for _ in range(request_num)
    ]
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f'{time.time()-start} seconds used.')
