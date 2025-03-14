import pathlib
from os import PathLike, walk
from collections.abc import Generator
from typing import NamedTuple


class HedEntry(NamedTuple):
    offset: int
    size: int
    path: pathlib.PureWindowsPath


def calc_padding(value: int, alignment: int) -> int:
    """Returns the padding needed to align a value to a specific boundary."""
    return (alignment - (value % alignment)) % alignment


def path_to_bytes(path: pathlib.Path, src_dir: pathlib.Path) -> bytes:
    """Converts a file path relative to the source directory to Windows-style
    path null terminated encoded as UTF-8.
    """
    return (
        f"{pathlib.PureWindowsPath('/') / path.relative_to(src_dir)}\0".encode(
            "utf-8"
        )
    )


def walk_files(directory: PathLike) -> Generator[pathlib.Path]:
    """Walks through a directory and yields only the files."""
    for root, _, files in walk(directory):
        for file in files:
            yield pathlib.Path(root) / file
