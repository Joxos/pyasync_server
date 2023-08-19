from loguru import logger
from sys import stderr

logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)

server_address = ('127.0.0.1', 1145)
