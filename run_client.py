"""
client.py: High-performance async client codes.
"""
from common.utils import handle_run_main
from loguru import logger
from client.package import pack_request_login
from client.config import SERVER_ADDRESS, CRT_PATH
from common.config import ENABLE_TLS
import asyncio
import ssl

from client.client import send_simple_package


async def main():
    context = None
    if ENABLE_TLS:
        context = ssl.create_default_context()
        context.check_hostname = False
        try:
            context.load_verify_locations(CRT_PATH)
        except FileNotFoundError:
            logger.error("File missing when using TLS.")
            return
        else:
            logger.info("TLS enabled.")
    else:
        logger.warning("TLS not enabled.")

    mypackage = pack_request_login("Joxos", "114514")
    await send_simple_package(mypackage, SERVER_ADDRESS, context)


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
