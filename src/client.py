import asyncio

from protocol import unpack_and_process, pack_change_question_mark, is_framed, on_init
from utils import *


class ClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.data = ''
        self.current_package_length = False
        on_init(self)

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        show_status(STATUS.CONNECTED, self.address)
        transport.write(compress(bytes(self.message, encoding=default_coding)))
        show_status(STATUS.SEND, self.address, self.message)

    def data_received(self, data):
        try:
            self.data += decompress(data).decode('utf-8')
        except:
            show_status(STATUS.ERROR, self.address,
                        'Failed to decompress or decode.')
            self.transport.close()
            return
        if is_framed(self):
            show_status(STATUS.RECV, self.address, self.data)
            res = unpack_and_process(self.data)
            self.transport.write(compress(bytes(res, encoding=default_coding)))
            show_status(STATUS.RECV, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = pack_change_question_mark('Hello there?')

    transport, protocol = await loop.create_connection(
        lambda: ClientProtocol(message, on_con_lost), server_address[0],
        server_address[1])

    try:
        await on_con_lost
    finally:
        transport.close()


if __name__ == '__main__':
    handle_run_main(main)
