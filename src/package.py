import json
from enum import Enum, auto


# low-level packers
class PACKAGE(Enum):
    CHANGE_QUESTION_MARK = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()
    UNKNOWN_PACKAGE_TYPE = auto()


def pack_json(obj):
    message = json.dumps(obj)
    return f'{len(message)}:{message}'


def split_package(data):
    index = data.find(':')
    return (int(data[:index]), data[index + 1:])


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
