import asyncio

from protocol import unpack_and_process, is_framed, on_init
from utils import *


# callback style server:
class ServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.data = ''
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        on_init(self)
        show_status(STATUS.CONNECTED, self.address)

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
            show_status(STATUS.SEND, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_status(STATUS.DISCONNECTED, self.address)


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: ServerProtocol(),
                                      server_address[0], server_address[1])
    logger.info(f'Listening at {server_address}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    handle_run_main(main)