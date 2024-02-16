import asyncio

from common.protocol import on_init, is_framed
from common.utils import (
    show_status,
    compress,
    decompress,
    STATUS,
)
from server.package import unpack_and_process
from server.config import *


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
