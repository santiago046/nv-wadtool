from collections import namedtuple


FileInfo = namedtuple("FileInfo", "data_offset, data_size, path")


def calc_padding(length: int, align: int) -> int:
    return (align - (length % align)) % align
