from utils import *
from protocol import pack_change_question_mark, unpack_and_process
import asyncio, time


class ClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.data = ''
        self.current_package_length = False

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        show_info(STATUS.CONNECTED, self.address)
        transport.write(bytes(self.message, encoding=default_coding))
        show_info(STATUS.SEND, self.address, self.message)

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
            show_info(STATUS.RECV, self.address, res)
            self.transport.close()

    def connection_lost(self, exc):
        show_info(STATUS.DISCONNECTED, self.address)
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('User exit.')
    except ConnectionRefusedError:
        logger.error(f'{server_address} refused to accept a connection.')
