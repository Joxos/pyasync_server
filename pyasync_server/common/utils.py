"""
utils.py: Common utils defines here.
"""
from asyncio import run
from loguru import logger
from pyasync_server.common.config import *
from pyasync_server.common.compress import compress
from pyasync_server.common.logging import show_status, STATUS
import ssl


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


def send_package(transport, protocol, package):
    transport.write(compress(bytes(package, encoding=DEFAULT_CODING)))
    show_status(STATUS.SEND, protocol.address, package)


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


def resolve_server_ssl_context(certfile, keyfile):
    context = None
    if ENABLE_TLS:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.check_hostname = False
        try:
            context.load_cert_chain(certfile, keyfile)
        except FileNotFoundError:
            logger.error("File missing when using TLS.")
            return
        else:
            logger.info("TLS enabled.")
    else:
        logger.warning("TLS not enabled.")
    return context
