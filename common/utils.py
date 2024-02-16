"""
utils.py: Common utils defines here.
"""
from asyncio import run
from enum import Enum, auto
from sys import stderr
from loguru import logger
from common.config import *
import ssl

# logger settings
logger.remove()
logger.add(
    stderr,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)

logger.info(f"{DEFAULT_COMPRESSER.name.lower().title()} compress selected.")
if DEFAULT_COMPRESSER == COMPRESSER.ZLIB:
    from zlib import compress, decompress
elif DEFAULT_COMPRESSER == COMPRESSER.GZIP:
    from gzip import compress, decompress
elif DEFAULT_COMPRESSER == COMPRESSER.BZ2:
    from bz2 import compress, decompress
elif DEFAULT_COMPRESSER == COMPRESSER.LZMA:
    from lzma import compress, decompress
elif DEFAULT_COMPRESSER == COMPRESSER.NONE:

    def compress(m):
        return m

    def decompress(m):
        return m


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


# console exception handler
def handle_run_main(main, server_address):
    try:
        run(main())
    except KeyboardInterrupt:
        logger.info("User exit.")
    except ConnectionRefusedError:
        logger.error(f"{server_address} refused to accept a connection.")
    except ConnectionResetError:
        logger.error(f"Connection to {server_address} was reset.")
        logger.info(
            "This might caused by that TLS support is enabled on the server but not on client."
        )

def send_package(transport, package):
    transport.write(compress(bytes(package, encoding=DEFAULT_CODING)))
    show_status(STATUS.SEND, transport.get_extra_info("peername"), package)

def resolve_client_ssl_context(certfile):
    context = None
    if ENABLE_TLS:
        context = ssl.create_default_context()
        context.check_hostname = False
        try:
            context.load_verify_locations(certfile)
        except FileNotFoundError:
            logger.error("File missing when using TLS.")
            return
        else:
            logger.info("TLS enabled.")
    else:
        logger.warning("TLS not enabled.")
    return context