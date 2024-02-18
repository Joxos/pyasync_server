"""
client.py: High-performance async client codes.
"""
import asyncio
from pyasync_server.common.protocol import on_init, is_framed
from pyasync_server.common.logging import show_status, STATUS
from pyasync_server.common.compress import decompress, compress
from pyasync_server.common.config import DEFAULT_CODING
from pyasync_server.client.package import unpack_and_process


class ClientProtocol(asyncio.Protocol):
    """Simple client protocol that can send packages and receive packages."""

    def __init__(self, result, is_lost):
        self.is_lost = is_lost
        self.received_data = ""
        self.result = result
        on_init(self)

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        show_status(STATUS.CONNECTED, self.address)

    def data_received(self, more_data):
        try:
            self.received_data += decompress(more_data).decode("utf-8")
        except:
            show_status(STATUS.ERROR, self.address, "Failed to decompress or decode.")
            self.transport.close()
            return
        if is_framed(self):
            show_status(STATUS.RECV, self.address, self.received_data)
            self.result.set_result(unpack_and_process(self.received_data))
            show_status(STATUS.RECV, self.address, self.result.result())

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)
        self.is_lost.set_result(True)


class Connection:
    """Connection class that can send and receive packages."""

    def __init__(self, server_address, ssl_context=None):
        self.server_address = server_address
        self.ssl_context = ssl_context
        self.transport = None
        self.protocol = None
        self.is_lost = None
        self.result = None

    async def establish(self):
        loop = asyncio.get_running_loop()
        self.is_lost = loop.create_future()
        self.result = loop.create_future()

        self.transport, self.protocol = await loop.create_connection(
            lambda: ClientProtocol(self.result, self.is_lost),
            self.server_address[0],
            self.server_address[1],
            ssl=self.ssl_context,
        )

    async def send_package(self, package):
        self.transport.write(compress(bytes(package, encoding=DEFAULT_CODING)))
        show_status(STATUS.SEND, self.protocol.address, package)

    async def receive_package(self):
        return await self.result

    async def close(self):
        self.transport.close()
        await self.is_lost
