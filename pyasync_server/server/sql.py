from enum import Enum, auto
from pyasync_server.common.logging import logger
from sys import exit


class SQLTYPE(Enum):
    NONE = auto()
    MYSQL = auto()
    MARIADB = auto()


SQL_TYPE = SQLTYPE.MARIADB

# resolve SQL connection
if SQL_TYPE == SQLTYPE.MYSQL:
    from pymysql import connect, Error
elif SQL_TYPE == SQLTYPE.MARIADB:
    from mariadb import connect, Error
elif SQL_TYPE == SQLTYPE.NONE:

    def connect(**kwargs):
        logger.error("No SQL selected. Cannot publish any connection.")
        exit(-1)

    class Error(Exception):
        pass


def establish_connection(user, password, address):
    try:
        conn = connect(user=user, password=password, host=address[0], port=address[1])
    except Error as e:
        logger.error(f"Error connecting to {SQL_TYPE.name.lower().title()}: {e}")
        exit(-1)
    logger.info(f"Successfully connected to {SQL_TYPE.name.lower().title()}.")
    return conn
