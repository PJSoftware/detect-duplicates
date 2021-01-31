from enum import IntEnum
import os

from .config import Verbosity
from . import config

def version():
    folder = os.path.abspath(os.path.dirname(__file__))
    with open(folder + '/VERSION') as f:
        version_data = f.read().splitlines()
        return version_data[0]

def recurse_into_folder(dir) -> dict:
    by_size = {}
    output(f"Searching in {dir}", Verbosity.Information)
    for entry in os.scandir(dir):
        if entry.is_file():
            size = os.path.getsize(entry.path)
            if size > 0:
                output(f"  {entry.path}: {size} bytes", Verbosity.Waffle)
                if size not in by_size:
                    by_size[size] = []
                by_size[size].append(entry.path)
        elif entry.is_dir():
            if entry.name[:1] == '.':
                output(f"Skipping folder {entry.path}", Verbosity.Detailed)
            elif entry.name == '_dup_archive':
                output(f"Skipping archive folder {entry.path}", Verbosity.Detailed)
            else:
                recurse_into_folder(entry.path)
    return by_size

def output(string: str, level: int = Verbosity.Required):
    if level <= config.VERBOSITY_LEVEL:
        print(string)
