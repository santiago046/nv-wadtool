import pathlib

import click

import nvwad


force_overwt = click.option(
    "-f", "--force", help="Overwrite existing output files.", is_flag=True
)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Pack or unpack Neversoft PS2 Engine WAD files.",
)
def nv_wadtool():
    pass


# --- Pack command --- #
@nv_wadtool.command(name="pack")
@force_overwt
@click.option(
    "-o",
    "--output",
    "out_wad",
    metavar="PATH",
    help="Specify the output WAD file. If not provided, defaults to './' + SRC_DIR base name with '.wad' extension.",
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    nargs=1,
)
@click.argument(
    "src_dir",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        readable=True,
        path_type=pathlib.Path,
    ),
)
def pack_wad(force, out_wad, src_dir):
    """Pack a directory into a Neversoft PS2 WAD file.

    SRC_DIR is the directory containing files to be packed.
    """
    if out_wad is None:
        out_wad = pathlib.Path("./", src_dir.stem).with_suffix(".wad")

    wad_path = out_wad
    hed_path = wad_path.with_suffix(".hed")

    if (hed_path.exists() or wad_path.exists()) and not force:
        raise FileExistsError(
            f"The destination WAD/HED file already exists. Use `-f/--force` to overwrite it."
        )

    with open(hed_path, "wb") as hed_file, open(wad_path, "wb") as wad_file:
        nvwad.pack(src_dir, hed_file, wad_file)


# --- Unpack command --- #
@nv_wadtool.command(name="unpack")
@force_overwt
@click.option(
    "-o",
    "--output",
    "out_dir",
    metavar="DIR",
    help="Specify the output directory. If not provided, defaults to './' + WAD_FILE base name without extension.",
    type=click.Path(dir_okay=True, file_okay=False, path_type=pathlib.Path),
    nargs=1,
)
@click.argument(
    "hed_path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.argument(
    "wad_path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
def unpack_wad(force, out_dir, hed_path, wad_path):
    """Unpack a Neversoft PS2 WAD file.

    \b
    HED_PATH is the path to a .hed (header) file.
    WAD_PATH is the path to a .wad file.
    """
    if not out_dir:
        out_dir = pathlib.Path("./", wad_path.stem)

    if out_dir.exists() and not force:
        raise FileExistsError(
            f"The destination output directory already exists. Use `-f/--force` to overwrite it."
        )

    with open(hed_path, "rb") as hed_path, open(wad_path, "rb") as wad_path:
        nvwad.unpack(hed_path, wad_path, out_dir)


if __name__ == "__main__":
    nv_wadtool()
