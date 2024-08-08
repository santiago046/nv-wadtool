"""
Provides functions and a CLI to pack and unpack Neversoft PS2 WAD files.
"""

from .nv_wadtool import nv_wadtool
from .pack import pack
from .unpack import unpack

__version__ = "1.0.1"

__all__ = ["pack, unpack"]
