'''
package.py: Define the format of different packages and ways to parse them.
'''
import json
from enum import Enum, auto
from actions import *


class PACKAGE(Enum):
    UNKNOWN_PACKAGE_TYPE = auto()
    CHANGE_QUESTION_MARK = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()
    MARIADB_TEST = auto()
    ANSWER_MARIADB_TEST = auto()


def pack_json(obj):
    message = json.dumps(obj)
    return f'{len(message)}:{message}'


# high-level package format defined here
def pack_unknown_package_type():
    return pack_json({'type': PACKAGE.UNKNOWN_PACKAGE_TYPE.name})


def pack_change_question_mark(sentence):
    return pack_json({
        'type': PACKAGE.CHANGE_QUESTION_MARK.name,
        'sentence': sentence
    })


def pack_answer_change_question_mark(sentence):
    return pack_json({
        'type': PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name,
        'sentence': sentence
    })


def pack_mariadb_test(sql):
    return pack_json({'type': PACKAGE.MARIADB_TEST.name, 'sql': sql})


def pack_answer_mariadb_test(result):
    return pack_json({'type': PACKAGE.ANSWER_MARIADB_TEST.name, 'result': result})


def unpack_and_process(package):
    '''Main logic to process every package.'''
    package = json.loads(package)
    package_type = package.get('type')
    if package_type == PACKAGE.CHANGE_QUESTION_MARK.name:
        return pack_answer_change_question_mark(
            change_question_mark(package.get('sentence')))
    elif package_type == PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name:
        return package.get('sentence')
    elif package_type == PACKAGE.MARIADB_TEST.name:
        return pack_answer_mariadb_test(mariadb_test(package.get('sql')))
    elif package_type == PACKAGE.ANSWER_MARIADB_TEST.name:
        return package.get('result')
    else:
        return pack_unknown_package_type()