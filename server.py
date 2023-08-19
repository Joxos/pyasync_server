from utils import logger, server_address
import protocol
import asyncio


# callback style server:
class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.data = ''
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        logger.info(f'--- {self.address}')

    def data_received(self, data):
        self.data += data.decode('utf-8')
        if self.data.endswith('?'):
            logger.info(f'<-- {self.address}: {self.data}')
            res = protocol.change_question_mark(self.data)
            self.transport.write(bytes(res, encoding='utf-8'))
            logger.info(f'--> {self.address}: {res}')
            self.transport.close()

    def connection_lost(self, exc):
        logger.info(f'- - {self.address}')


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: EchoServerProtocol(),
                                      server_address[0], server_address[1])
    logger.info(f'Listening at {server_address}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('User exit.')

# coroutine style server:
# async def handel_conversation(reader, writer):
#     address = writer.get_extra_info('peername')
#     logger.info(f'{address}: Connected.')
#     while True:
#         data = ''
#         while not data.endswith('?'):
#             more_data = await reader.read(1024)
#             if not more_data:
#                 if data:
#                     logger.error(f'{address}: Sent {data} but then closed.')
#                 else:
#                     logger.info(f'{address}: Closed.')
#                 return
#             data += more_data.decode('utf-8')
#             logger.info(f'{address}: {data}')
#         writer.write(bytes(data[:-1] + '!', encoding='utf-8'))
#         await writer.drain()

# async def main():
#     address = ('127.0.0.1', 1145)
#     server = await asyncio.start_server(handel_conversation, *address)
#     async with server:
#         logger.info(f'Listening at {address}')
#         await server.serve_forever()

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logger.info('User exit.')
