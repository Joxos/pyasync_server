import asyncio
from common.protocol import on_init, is_framed
from common.utils import (
    show_status,
    compress,
    decompress,
    STATUS,
)
from client.package import unpack_and_process
from common.config import DEFAULT_CODING


class ClientProtocol(asyncio.Protocol):
    def __init__(self, package_to_send, on_con_lost):
        self.package_to_send = package_to_send
        self.on_con_lost = on_con_lost
        self.received_data = ""
        on_init(self)

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        show_status(STATUS.CONNECTED, self.address)
        transport.write(compress(bytes(self.package_to_send, encoding=DEFAULT_CODING)))
        show_status(STATUS.SEND, self.address, self.package_to_send)

    def data_received(self, more_data):
        try:
            self.received_data += decompress(more_data).decode("utf-8")
        except:
            show_status(STATUS.ERROR, self.address, "Failed to decompress or decode.")
            self.transport.close()
            return
        if is_framed(self):
            show_status(STATUS.RECV, self.address, self.received_data)
            res = unpack_and_process(self.received_data)
            show_status(STATUS.RECV, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)
        self.on_con_lost.set_result(True)

async def send_simple_package(package_to_send, server_address,ssl_context=None):
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: ClientProtocol(package_to_send, on_con_lost),
        server_address[0],
        server_address[1],
        ssl=ssl_context,
    )

    try:
        await on_con_lost
    finally:
        transport.close()