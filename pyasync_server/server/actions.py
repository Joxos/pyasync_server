"""
actions.py: Main logic of actions to process after received packages.
"""
import json
import os
from pyasync_server.common.logging import logger
from pyasync_server.server.sql import establish_connection

SERVER_ADDRESS = ("127.0.0.1", 1145)
SQL_ADDRESS = ("192.168.2.115", 3306)
SQL_USER = "root"
SQL_PASSWORD = "123456"


def change_question_mark(sentence):
    return sentence[:-1] + "!"


def database_test(sql):
    conn = establish_connection(SQL_USER, SQL_PASSWORD, SQL_ADDRESS)
    cur = conn.cursor()
    cur.execute(sql)
    res = ""
    for d in cur:
        res += d[0] + "\n"
    return res[:-1]


# write your own actions here
def login(username, password):
    if not os.path.exists("./users.json"):
        logger.error("users.json not found. Cannot login.")
        return False
    with open("users.json", "r") as f:
        users = json.load(f)
    if username in users and users[username] == password:
        logger.info(f"User {username} logged in.")
        return True
    else:
        logger.error(f"Invalid username or password for user {username}.")
        return False


def register(username, password):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({username: password}, f)
        return True
    with open("users.json", "r") as f:
        users = json.load(f)
    if username in users:
        return False
    else:
        users[username] = password
        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
