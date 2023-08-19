from utils import logger, server_address
import asyncio, time


# callback style client:
class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.data = ''

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        logger.info(f'--- {self.address}')
        transport.write(self.message.encode('utf-8'))
        logger.info(f'--> {self.address}: {self.message}')

    def data_received(self, data):
        self.data += data.decode('utf-8')
        if self.data.endswith('!'):
            logger.info(f'<-- {self.address}: {self.data}')
            self.transport.close()

    def connection_lost(self, exc):
        logger.info(f'- - {self.address}')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello there?'

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost), server_address[0],
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
