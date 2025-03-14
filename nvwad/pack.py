import struct
from pathlib import Path
from typing import BinaryIO

from .constants import *
from .utils import *


def pack(
    src_dir: Path,
    hed_fp: BinaryIO,
    wad_fp: BinaryIO,
    sector_offsets: bool = False,
) -> None:
    """
    Packs a directory into a Neversoft PS2 WAD (Where's All Data) file.

    Args:
        src_dir: The directory path to be packed.
        hed_fp: The HED (header) file pointer opened in w+b mode.
        wad_fp: The WAD file pointer opened in w+b mode.
        sector_offsets: Use sector-based offsets in HED file.
    """
    offset = 0
    hed_buffer = bytearray()

    for file_path in walk_files(src_dir):
        hed_buffer.extend(
            struct.pack(
                "<II",
                offset // SECTOR_SIZE if sector_offsets else offset,
                file_size := file_path.stat().st_size,
            )
        )
        hed_buffer.extend(path_to_bytes(file_path, src_dir))
        hed_buffer.extend(
            bytearray(calc_padding(len(hed_buffer), HED_ALIGNMENT))
        )

        with file_path.open("rb") as file:
            while chunk := file.read(CHUNK_SIZE):
                wad_fp.write(chunk)

            wad_fp.write(
                bytearray(padding_size := calc_padding(file_size, SECTOR_SIZE))
            )

        offset += file_size + padding_size

    hed_fp.write(hed_buffer)
    hed_fp.write(HED_EOF)


__all__ = ["pack"]
