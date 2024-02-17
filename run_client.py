"""
run_client.py: An example of how to run a client.
"""
from pyasync_server.common.utils import handle_run_main, resolve_client_ssl_context
from pyasync_server.client.package import pack_request_login
from pyasync_server.client.client import send_simple_package

CRT_PATH = "server.crt"
SERVER_ADDRESS = ("127.0.0.1", 1145)


async def main():
    ssl_context = resolve_client_ssl_context(CRT_PATH)
    mypackage = pack_request_login("Joxos", "114514")
    result = await send_simple_package(mypackage, SERVER_ADDRESS, ssl_context)
    print(result.result())


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
