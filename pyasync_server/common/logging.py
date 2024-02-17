from enum import Enum, auto
from loguru import logger
from sys import stderr

# logger settings
logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)


# console banners
class STATUS(Enum):
    SEND = auto()
    RECV = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()
    ERROR = auto()


def show_status(direction, address, message=""):
    if direction == STATUS.RECV:
        logger.info(f"<-- {address} {message}")
    elif direction == STATUS.SEND:
        logger.info(f"--> {address} {message}")
    elif direction == STATUS.CONNECTED:
        logger.info(f"--- {address} {message}")
    elif direction == STATUS.DISCONNECTED:
        logger.info(f"-x- {address} {message}")
    elif direction == STATUS.ERROR:
        logger.error(f"xxx {address} {message}")
