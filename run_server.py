"""
run_server.py: An example of how to run the server.
"""
from pyasync_server.common.utils import handle_run_main, resolve_server_ssl_context
from loguru import logger
from pyasync_server.server.config import (
    CRT_PATH,
    KEY_PATH,
    SERVER_ADDRESS,
)
import asyncio
from pyasync_server.server.server import ServerProtocol


async def main():
    context = resolve_server_ssl_context(CRT_PATH, KEY_PATH)

    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: ServerProtocol(), SERVER_ADDRESS[0], SERVER_ADDRESS[1], ssl=context
    )

    logger.info(f"Listening at {SERVER_ADDRESS}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    handle_run_main(main, SERVER_ADDRESS)
