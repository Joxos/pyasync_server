from enum import Enum, auto


class COMPRESSER(Enum):
    ZLIB = auto()
    GZIP = auto()
    BZ2 = auto()
    LZMA = auto()
    NONE = auto()


compresser = COMPRESSER.NONE
server_address = ('127.0.0.1', 1145)
default_coding = 'utf-8'
