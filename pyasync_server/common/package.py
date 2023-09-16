'''
package.py: Define the format of different packages and ways to parse them.
'''
from enum import Enum, auto
import json


def pack_json(obj):
    message = json.dumps(obj)
    return f'{len(message)}:{message}'


class PACKAGE(Enum):
    UNKNOWN_PACKAGE_TYPE = auto()
    REQUEST_CHANGE_QUESTION_MARK = auto()
    REQUEST_MARIADB_TEST = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()
    ANSWER_MARIADB_TEST = auto()
