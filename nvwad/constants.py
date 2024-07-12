"""Constants used by pack and unpack funtions"""


class Constants:
    # File reading and writing
    CHUNK_SIZE = 2**20  # 1MB

    # HED file
    FILE_ENTRY_ALIGN = 4
    HED_END_MARKER = b"\xff" * 4

    # WAD file
    WAD_DATA_ALIGN = 2048
