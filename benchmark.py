import time
from threading import Thread

from client import main, server_address
from utils import handle_run_main

REQUEST_NUM = 1000

if __name__ == "__main__":
    threads = [
        Thread(target=handle_run_main, args=(main, server_address))
        for _ in range(REQUEST_NUM)
    ]
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"{time.time()-start} seconds used.")
