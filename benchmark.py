import asyncio, time
from client import main
from utils import handle_run_main
from threading import Thread

request_num = 1000

if __name__ == '__main__':
    threads = [
        Thread(target=handle_run_main, args=(main, ))
        for _ in range(request_num)
    ]
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f'{time.time()-start} seconds used.')
