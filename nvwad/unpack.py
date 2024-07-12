import pathlib
import struct
from collections.abc import Iterator
from typing import BinaryIO

from .constants import Constants
from .utils import calc_padding, FileInfo


__all__ = ["unpack"]


def parse_hed(hed_fp: BinaryIO) -> Iterator[FileInfo]:
    """
    Parses a Neversoft PS2 HED (header) file and yields file entries.

    This function reads the HED file, extracts file entries including data
    offset, size, and path, and yields them as FileInfo named tuples.

    Args:
        hed_fp (BinaryIO): The HED (header) file pointer opened in r+b mode.

    Yields:
        FileInfo: A named tuple containing the data offset, data size, and
          file path.
    """
    while (chunk := hed_fp.read(8)) != Constants.HED_END_MARKER:
        data_offset, data_size = struct.unpack("<II", chunk)
        file_path = b""
        while (b := hed_fp.read(1)) != b"\x00":
            file_path += b

        entry_length = len(chunk + file_path + b"\x00")
        padding_length = calc_padding(entry_length, Constants.FILE_ENTRY_ALIGN)
        hed_fp.read(padding_length)

        file_path = pathlib.PureWindowsPath(file_path.decode("ascii"))

        yield FileInfo(data_offset, data_size, file_path)


def unpack(hed_fp: BinaryIO, wad_fp: BinaryIO, dst_dir: pathlib.Path) -> None:
    """
    Unpacks the contents of a Neversoft PS2 WAD file into a specified directory.

    This function reads entries from the HED (header) file and extracts
    corresponding data from the WAD (Where's All the Data) file, writing each
    file to the specified directory.

    Args:
        hed_fp (BinaryIO): The HED (header) file pointer opened in r+b mode.
        wad_fp (BinaryIO): The WAD file pointer opened in r+b mode.
        dst_dir (pathlib.Path): The destination directory where the files will
          be extracted.
    """
    for file_entry in parse_hed(hed_fp):
        output_path = dst_dir / file_entry.path.relative_to("\\")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        wad_fp.seek(file_entry.data_offset)

        with open(output_path, "wb") as out_file:
            bytes_remaining = file_entry.data_size

            while bytes_remaining > 0:
                chunk_size = min(Constants.CHUNK_SIZE, bytes_remaining)
                chunk = wad_fp.read(chunk_size)
                out_file.write(chunk)
                bytes_remaining -= len(chunk)
