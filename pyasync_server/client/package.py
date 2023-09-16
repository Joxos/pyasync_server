'''
package.py: Define the format of different packages and ways to parse them.
'''
import json
from enum import Enum, auto
from common.package import pack_json, PACKAGE
from actions import *


def pack_unknown_package_type():
    return pack_json({'type': PACKAGE.UNKNOWN_PACKAGE_TYPE.name})


def pack_request_change_question_mark(sentence):
    return pack_json({
        'type': PACKAGE.REQUEST_CHANGE_QUESTION_MARK.name,
        'sentence': sentence
    })


def pack_request_mariadb_test(sql):
    return pack_json({'type': PACKAGE.REQUEST_MARIADB_TEST.name, 'sql': sql})


def unpack_and_process(package):
    '''Main logic to process every package.'''
    package = json.loads(package)
    package_type = package.get('type')
    if package_type == PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name:
        return package.get('sentence')
    elif package_type == PACKAGE.ANSWER_MARIADB_TEST.name:
        return package.get('result')
    else:
        return pack_unknown_package_type()