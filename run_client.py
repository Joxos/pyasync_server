"""
client.py: High-performance async client codes.
"""
from common.utils import handle_run_main, logger
from client.package import pack_request_login
from client.config import SERVER_ADDRESS, ENABLE_TLS, CRT_PATH
import asyncio
import ssl

from client.client import ClientProtocol


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

    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    mypackage = pack_request_login("Joxos", "114514")

    transport, protocol = await loop.create_connection(
        lambda: ClientProtocol(mypackage, on_con_lost),
        SERVER_ADDRESS[0],
        SERVER_ADDRESS[1],
        ssl=context,
    )

    try:
        await on_con_lost
    finally:
        transport.close()


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
