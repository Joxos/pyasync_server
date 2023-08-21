import json
from enum import Enum, auto
from utils import show_status, STATUS, compress, decompress
from config import default_coding


# packers
class PACKAGE(Enum):
    CHANGE_QUESTION_MARK = auto()
    ANSWER_CHANGE_QUESTION_MARK = auto()


def pack_json(obj):
    message = json.dumps(obj)
    return f'{len(message)}:{message}'


def split_package(data):
    index = data.find(':')
    return (int(data[:index]), data[index + 1:])


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


#low-level protocol content
def on_init(sp):
    sp.current_package_length = False


def is_framed(sp):
    if not sp.current_package_length and ':' in sp.data:
        sp.current_package_length, sp.data = split_package(sp.data)
    # package length satisfied
    if len(sp.data) != 0 and len(sp.data) == sp.current_package_length:
        show_status(STATUS.RECV, sp.address, sp.data)
        res = unpack_and_process(sp.data)
        sp.transport.write(compress(bytes(res, encoding=default_coding)))
        show_status(STATUS.SEND, sp.address, res)
        sp.transport.close()


# protocol actions
def change_question_mark(sentence):
    return sentence[:-1] + '!'