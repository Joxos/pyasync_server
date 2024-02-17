"""
server.py: High-performance async server codes.
"""
import asyncio

from pyasync_server.common.protocol import on_init, is_framed
from pyasync_server.common.logging import (
    show_status,
    STATUS,
)
from pyasync_server.common.compress import compress, decompress
from pyasync_server.server.package import unpack_and_process
from pyasync_server.common.config import DEFAULT_CODING


# callback style server:
class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.received_data = ""
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        on_init(self)
        show_status(STATUS.CONNECTED, self.address)

    def data_received(self, more_data):
        try:
            self.received_data += decompress(more_data).decode("utf-8")
        except:
            show_status(
                STATUS.ERROR, self.address, "Failed to decompress or decode more data."
            )
            self.transport.close()
            return
        if is_framed(self):
            show_status(STATUS.RECV, self.address, self.received_data)
            # transfer control to actions.py
            res = unpack_and_process(self.received_data)
            self.transport.write(compress(bytes(res, encoding=DEFAULT_CODING)))
            show_status(STATUS.SEND, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)
