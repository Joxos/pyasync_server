"""
protocol.py: Define how to frame a package.
"""


def on_init(sp):
    sp.current_package_length = False


def is_framed(sp):
    if not sp.current_package_length and ":" in sp.received_data:
        sp.current_package_length, sp.received_data = split_package(sp.received_data)
    # package length satisfied
    if (
        len(sp.received_data) != 0
        and len(sp.received_data) == sp.current_package_length
    ):
        return True
    return False


def split_package(data):
    index = data.find(":")
    return (int(data[:index]), data[index + 1 :])
