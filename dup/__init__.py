from enum import IntEnum
import os

from .config import Verbosity
from . import config
from . import global_var

def version() -> str:
    """returns version information read from VERSION file"""
    folder = os.path.abspath(os.path.dirname(__file__))
    with open(folder + '/VERSION') as f:
        version_data = f.read().splitlines()
        return version_data[0]

def recurse_into_folder(dir) -> dict:
    """find all files under current folder and group by size"""
    by_size = {}
    output(f"Searching in {dir}", Verbosity.Information)
    for entry in os.scandir(dir):
        if entry.is_file():
            size = os.path.getsize(entry.path)
            if size > 0 or not config.IGNORE_ZERO_LENGTH:
                output(f"  {entry.path}: {size} bytes", Verbosity.Waffle)
                if size not in by_size:
                    by_size[size] = []
                else:
                    global_var.size_matched += 1
                by_size[size].append(entry.path)
                global_var.files_found += 1
        elif entry.is_dir():
            if entry.name[:1] == '.' and not config.INCLUDE_HIDDEN:
                output(f"Skipping hidden folder {entry.path}", Verbosity.Detailed)
            elif entry.name == '.git':
                output(f"Skipping hidden .git folder despite --hidden flag", Verbosity.Detailed)
            elif entry.name == config.ARCHIVE_FOLDER:
                output(f"Skipping archive folder {entry.path}", Verbosity.Detailed)
            else:
                recurse_into_folder(entry.path)
    return by_size

def output(string: str, level: int = Verbosity.Required):
    """print string if specified level allowed by VERBOSITY settings"""
    if level <= config.VERBOSITY_LEVEL:
        print("  "*level + string)
