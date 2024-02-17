from loguru import logger
from pyasync_server.common.config import DEFAULT_COMPRESSER, COMPRESSER


# resolve compressor
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
