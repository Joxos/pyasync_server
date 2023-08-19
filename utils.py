from loguru import logger
from enum import Enum, auto
from sys import stderr

logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)

server_address = ('127.0.0.1', 1145)


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
        logger.info(f'- - {address} {message}')
