'''
actions.py: Main logic of actions to process after recieved packages.
'''
from common.utils import logger
from sys import exit
from config import *
if sql_type == SQLTYPE.MYSQL:
    from pymysql import connect, Error
elif sql_type == SQLTYPE.MARIADB:
    from mariadb import connect, Error
elif sql_type == SQLTYPE.NONE:

    def connect(**kwargs):
        logger.error('No SQL selected. Cannot publish any connection.')
        exit(-1)

    class Error(Exception):
        pass


def change_question_mark(sentence):
    return sentence[:-1] + '!'


def database_test(sql):
    try:
        conn = connect(user=sql_user,
                       password=sql_password,
                       host=sql_address,
                       port=sql_port)
    except Error as e:
        logger.error(
            f'Error connecting to {sql_type.name.lower().title()}: {e}')
        return ''
    logger.info(f'Successfully connected to {sql_type.name.lower().title()}.')
    cur = conn.cursor()
    cur.execute(sql)
    res = ''
    for d in cur:
        res += d[0] + '\n'
    return res[:-1]
