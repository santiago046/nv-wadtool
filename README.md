# nv-wadtool
A Python CLI tool for packing and unpacking Neversoft PS2 Engine WAD files.

Neversoft PS2 WAD (Where's All the Data) files are used in various PlayStation 2 games that use Neversoft Engine, such as Tony Hawk's Pro Skater series, GUN and MTX Mototrax. These files contain game resources like textures, models, sound files, and other assets.

## Installation
To install `nv-wadtool`, you can use pip. Follow these steps:

1. Clone this repository:
   ```
   git clone https://github.com/santiago046/nv-wadtool
   ```
2. Change to the project directory:
   ```
   cd nv-wadtool
   ```
3. Install using pip
   ```
   pip install .
   ```

## Usage
`nv-wadtool` has two commands: `pack` and `unpack`.

### Pack Command

The `pack` command takes a directory containing files and/or subdirectories and packs them into a WAD file along with its .HED file.
```
Usage: nv-wadtool pack [OPTIONS] SRC_DIR

  Pack a directory into a Neversoft PS2 WAD file.

  SRC_DIR is the directory containing files to be packed.

Options:
  -f, --force        Overwrite existing output files.
  -o, --output PATH  Specify the output WAD file. If not provided, defaults to
                     './' + SRC_DIR base name with '.wad' extension.
  -h, --help         Show this message and exit.
```

### Unpack Command

The `unpack` command takes a HED and WAD files and unpack contents from it.
```
Usage: nv-wadtool unpack [OPTIONS] HED_PATH WAD_PATH

  Unpack a Neversoft PS2 WAD file.

  HED_PATH is the path to a .hed (header) file.
  WAD_PATH is the path to a .wad file.

Options:
  -f, --force       Overwrite existing output files.
  -o, --output DIR  Specify the output directory. If not provided, defaults to
                    './' + WAD_FILE base name without extension.
  -h, --help        Show this message and exit.
```

## Examples

### Packing a Directory

- To pack a directory named "music" into a WAD file, creating `music.wad` and `music.hed` in the current directory:
   ```
   nv-wadtool pack music
   ```

- To specify a different output file:
   ```
   nv-wadtool pack music -o /path/to/output/custom_name.wad
   ```

### Unpacking a WAD File

- To unpack a WAD file to a directory named "game" in the current directory:
   ```
   nv-wadtool unpack game.hed game.wad
   ```

- To specify a different output directory:
   ```
   nv-wadtool unpack game.hed game.wad -o /path/to/output/extracted_assets
   ```

### Force Overwrite

- To overwrite existing files when packing or unpacking, use the `-f` or `--force` option:
   ```
   nv-wadtool pack music -f
   nv-wadtool unpack game.hed game.wad -f
   ```

## License
nv-wadtool is released under MIT license.

See the file [LICENSE](LICENSE) for more details.
