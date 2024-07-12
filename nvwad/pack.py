import os
import pathlib
import struct
from collections.abc import Iterator
from typing import BinaryIO

from .constants import Constants
from .utils import FileInfo, calc_padding


__all__ = ["pack"]


def pack(src_dir: pathlib.Path, hed_fp: BinaryIO, wad_fp: BinaryIO) -> None:
    """
    Packs a directory into a Neversoft PS2 WAD (Where's All Data) file.

    This function scans a directory for files, packs them, and writes the data
    to HED (header) and WAD (Where's All Data) files.

    Args:
        src_dir (pathlib.Path): The directory path to be packed.
        hed_fp (BinaryIO): The HED (header) file pointer opened in w+b mode.
        wad_fp (BinaryIO): The WAD file pointer opened in w+b mode.
    """

    def convert_path(file_path: pathlib.Path) -> bytes:
        """Convert a file path to a Windows-style path encoded in UTF-8."""
        file_path = pathlib.PureWindowsPath("/") / file_path.relative_to(
            src_dir
        )
        return str(file_path).encode("utf-8") + b"\x00"

    def get_all_files() -> Iterator[pathlib.Path]:
        """Recursively yield all files in the given directory."""
        for root, _, files in os.walk(src_dir):
            for file in files:
                yield pathlib.Path(root) / file

    file_offset = 0

    for file_path in get_all_files():
        file_size = file_path.stat().st_size
        converted_path = convert_path(file_path)

        # Write file entry in the HED file
        file_entry = struct.pack("<II", file_offset, file_size) + converted_path
        entry_pad_len = calc_padding(
            len(file_entry), Constants.FILE_ENTRY_ALIGN
        )
        hed_fp.write(file_entry + (entry_pad_len * b"\x00"))

        # Write file data in the WAD file
        with open(file_path, "rb") as data:
            while chunk := data.read(Constants.CHUNK_SIZE):
                wad_fp.write(chunk)
            data_pad_len = calc_padding(file_size, Constants.WAD_DATA_ALIGN)
            wad_fp.write(data_pad_len * b"\x00")

        file_offset += file_size + data_pad_len

    # Finish the HED file
    hed_fp.write(Constants.HED_END_MARKER)
