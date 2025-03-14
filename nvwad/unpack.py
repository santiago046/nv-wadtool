import struct
from collections.abc import Generator
from os import SEEK_CUR
from pathlib import Path, PureWindowsPath
from typing import BinaryIO

from .constants import *
from .utils import calc_padding, HedEntry


def parse_hed(hed_fp: BinaryIO) -> tuple[HedEntry, ...]:
    """
    Parses a Neversoft PS2 HED (header) file and yields entries.

    Args:
        hed_fp: The HED (header) file pointer opened in r+b mode.

    Returns:
        A tuple of named tuples containing offset, size, and path.
    """
    entries = []
    path_buf = bytearray()

    while chunk := hed_fp.read(8):
        if chunk == HED_EOF:
            break

        offset, size = struct.unpack("<II", chunk)

        while (byte := hed_fp.read(1)) != b"\x00":
            path_buf.extend(byte)

        hed_fp.seek(
            calc_padding(
                len(chunk) + len(path_buf) + 1,  # +1 for null byte
                HED_ALIGNMENT,
            ),
            SEEK_CUR,
        )

        entries.append(
            HedEntry(offset, size, PureWindowsPath(path_buf.decode("ascii")))
        )
        path_buf.clear()

    return tuple(entries)


def unpack(hed_fp: BinaryIO, wad_fp: BinaryIO, dst_dir: Path) -> None:
    """
    Unpacks the contents of a Neversoft PS2 WAD file into a specified directory.

    Args:
        hed_fp: The HED (header) file pointer opened in r+b mode.
        wad_fp: The WAD file pointer opened in r+b mode.
        dst_dir: The destination directory where the files will be extracted.
    """
    hed_entries = parse_hed(hed_fp)

    is_sector_offsets = hed_entries[1].offset < hed_entries[0].size
    if is_sector_offsets:
        print("Note: This WAD file uses sector-based offsets.")

    for hed_entry in hed_entries:
        output_path = dst_dir / hed_entry.path.relative_to("\\")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        wad_fp.seek(
            hed_entry.offset * SECTOR_SIZE
            if is_sector_offsets
            else hed_entry.offset
        )

        with output_path.open("wb") as out_file:
            remaining = hed_entry.size

            while remaining > 0:
                chunk = wad_fp.read(min(CHUNK_SIZE, remaining))

                out_file.write(chunk)
                remaining -= len(chunk)


__all__ = ["unpack"]
