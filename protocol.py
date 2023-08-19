import json
from enum import Enum, auto


class PACKAGE(Enum):
    CHANGE_QUESTION_MARK = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()


def change_question_mark(sentence):
    return sentence[:-1] + '!'


def pack_json(obj):
    message = json.dumps(obj)
    return bytes(f'{len(message)}:{message}', encoding='utf-8')


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


def unpack_and_process(package):
    package = json.loads(package)
    if package.get('type') == PACKAGE.CHANGE_QUESTION_MARK.name:
        return pack_answer_change_question_mark(
            change_question_mark(package.get('sentence')))
    elif package.get('type') == PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name:
        return package.get('sentence')
