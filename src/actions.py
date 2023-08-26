'''
actions.py: Main logic of actions to process after recieved packages.
'''
import json
from package import *


def change_question_mark(sentence):
    return sentence[:-1] + '!'


def unpack_and_process(package):
    '''Main logic to process every package.'''
    package = json.loads(package)
    if package.get('type') == PACKAGE.CHANGE_QUESTION_MARK.name:
        return pack_answer_change_question_mark(
            change_question_mark(package.get('sentence')))
    elif package.get('type') == PACKAGE.ANSWER_CHANGE_QUESTION_MARK.name:
        return package.get('sentence')
    else:
        return pack_unknown_package_type()