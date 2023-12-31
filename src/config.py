'''
config.py: Configuration defines here.
'''
from enum import Enum, auto


class COMPRESSER(Enum):
    NONE = auto()
    ZLIB = auto()
    GZIP = auto()
    BZ2 = auto()
    LZMA = auto()


class SQLTYPE(Enum):
    NONE=auto()
    MYSQL = auto()
    MARIADB = auto()


# configuration starts here
compresser = COMPRESSER.NONE
default_coding = 'utf-8'
enable_tls = False
