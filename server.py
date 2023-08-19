from utils import *
from protocol import unpack_and_process
import asyncio


# callback style server:
class ServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.data = ''
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.current_package_length = False
        show_info(STATUS.CONNECTED, self.address)

    def data_received(self, data):
        self.data += data.decode('utf-8')
        # get package length first
        if not self.current_package_length and ':' in self.data:
            index = self.data.find(':')
            self.current_package_length, self.data = int(
                self.data[:index]), self.data[index + 1:]
        # package length satisfied
        if len(self.data) != 0 and len(
                self.data) == self.current_package_length:
            show_info(STATUS.RECV, self.address, self.data)
            res = unpack_and_process(self.data)
            self.transport.write(bytes(res, encoding=default_coding))
            show_info(STATUS.SEND, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_info(STATUS.DISCONNECTED, self.address)


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: ServerProtocol(),
                                      server_address[0], server_address[1])
    logger.info(f'Listening at {server_address}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('User exit.')
