"""
client.py: High-performance async client codes.
"""
import asyncio
from pyasync_server.common.protocol import on_init, is_framed
from pyasync_server.common.utils import send_package
from pyasync_server.common.logging import show_status, STATUS
from pyasync_server.common.compress import decompress
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


async def send_simple_package(package_to_send, server_address, ssl_context=None):
    loop = asyncio.get_running_loop()
    is_lost = loop.create_future()
    result = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: ClientProtocol(result, is_lost),
        server_address[0],
        server_address[1],
        ssl=ssl_context,
    )

    send_package(transport, protocol, package_to_send)
    await result
    transport.close()
    return result
