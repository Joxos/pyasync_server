from package import *
from actions import unpack_and_process
from utils import show_status, STATUS, compress, decompress
from config import default_coding


# low-level protocol content
def on_init(sp):
    sp.current_package_length = False


def is_framed(sp):
    if not sp.current_package_length and ':' in sp.recieved_data:
        sp.current_package_length, sp.recieved_data = split_package(
            sp.recieved_data)
    # package length satisfied
    if len(sp.recieved_data) != 0 and len(
            sp.recieved_data) == sp.current_package_length:
        return True
    return False
