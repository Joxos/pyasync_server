from config import *
from asyncio import run
from loguru import logger
from enum import Enum, auto
from sys import stderr
from importlib import import_module

logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)

logger.info(f'{compresser.name.lower()} compress selected.')
if compresser == COMPRESSER.ZLIB:
    from zlib import compress, decompress
elif compresser == COMPRESSER.GZIP:
    from gzip import compress, decompress
elif compresser == COMPRESSER.BZ2:
    from bz2 import compress, decompress
elif compresser == COMPRESSER.LZMA:
    from lzma import compress, decompress
elif compresser == COMPRESSER.NONE:

    def compress(b):
        return b

    def decompress(b):
        return b


class STATUS(Enum):
    SEND = auto()
    RECV = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()


def show_info(direction, address, message=''):
    if direction == STATUS.RECV:
        logger.info(f'<-- {address} {message}')
    elif direction == STATUS.SEND:
        logger.info(f'--> {address} {message}')
    elif direction == STATUS.CONNECTED:
        logger.info(f'--- {address} {message}')
    elif direction == STATUS.DISCONNECTED:
        logger.info(f'-x- {address} {message}')


def split_package(data):
    index = data.find(':')
    return (int(data[:index]), data[index + 1:])


def handle_run_main(main):
    try:
        run(main())
    except KeyboardInterrupt:
        logger.info('User exit.')
    except ConnectionRefusedError:
        logger.error(f'{server_address} refused to accept a connection.')
