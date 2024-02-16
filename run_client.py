"""
client.py: High-performance async client codes.
"""
from common.utils import handle_run_main,resolve_client_ssl_context
from loguru import logger
from client.package import pack_request_login
from client.config import SERVER_ADDRESS, CRT_PATH

from client.client import send_simple_package


async def main():
    context = resolve_client_ssl_context(CRT_PATH)
    mypackage = pack_request_login("Joxos", "114514")
    result = await send_simple_package(mypackage, SERVER_ADDRESS, context)
    print(result)


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
