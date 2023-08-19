from utils import *
import asyncio, time


# callback style client:
class ClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.data = ''

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        show_info(STATUS.CONNECTED, self.address)
        transport.write(self.message.encode('utf-8'))
        show_info(STATUS.SEND, self.address, self.message)

    def data_received(self, data):
        self.data += data.decode('utf-8')
        if self.data.endswith('!'):
            show_info(STATUS.RECV, self.address, self.data)
            self.transport.close()

    def connection_lost(self, exc):
        show_info(STATUS.DISCONNECTED, self.address)
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello there?'

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
        print('User exit.')
