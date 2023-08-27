'''
actions.py: Main logic of actions to process after recieved packages.
'''
from utils import logger
from mariadb import connect, Error


def change_question_mark(sentence):
    return sentence[:-1] + '!'


def mariadb_test(sql):
    try:
        conn = connect(user='root',
                       password='123456',
                       host='192.168.2.115',
                       port=3306)
    except Error as e:
        logger.error(f'Error connecting to MariaDB: {e}')
        return
    logger.info(f'Successfully connected to MariaDB.')
    cur = conn.cursor()
    cur.execute(sql)
    res = ''
    for d in cur:
        res += d[0] + '\n'
    return res
