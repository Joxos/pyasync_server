'''
package.py: Define the format of different packages and ways to parse them.
'''
import json
from enum import Enum, auto


class PACKAGE(Enum):
    CHANGE_QUESTION_MARK = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()
    UNKNOWN_PACKAGE_TYPE = auto()


def pack_json(obj):
    message = json.dumps(obj)
    return f'{len(message)}:{message}'


# high-level package format defined here
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


def pack_unknown_package_type():
    return pack_json({'type': PACKAGE.UNKNOWN_PACKAGE_TYPE.name})
