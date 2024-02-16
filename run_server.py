"""
server.py: High-performance async server codes.
"""
import ssl
import sys

sys.path.append("..")
from common.utils import handle_run_main, logger
from server.config import (
    ENABLE_TLS,
    CRT_PATH,
    KEY_PATH,
    SERVER_ADDRESS,
)
import asyncio
from server.server import ServerProtocol


async def main():
    context = None
    if ENABLE_TLS:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.check_hostname = False
        try:
            context.load_cert_chain(CRT_PATH, KEY_PATH)
        except FileNotFoundError:
            logger.error("File missing when using TLS.")
            return
        else:
            logger.info("TLS enabled.")
    else:
        logger.warning("TLS not enabled.")

    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: ServerProtocol(), SERVER_ADDRESS[0], SERVER_ADDRESS[1], ssl=context
    )

    logger.info(f"Listening at {SERVER_ADDRESS}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
