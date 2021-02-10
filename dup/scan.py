import os

from .output import output
from . import config, progress
from .config import Verbosity

class File_Data():
    _name = ''
    _path = ''
    _ext = ''
    _size = 0
    _hash = ''

    def __init__(self, name: str, path: str, ext: str, size: int):
        self._name = name
        self._path = path
        self._ext = ext
        self._size = size

class Folder_Data():
    _tree_by_size = {}
    _total_size = 0
    _files_found = 0
    _files_rejected_size = 0
    _files_rejected_cat = 0
    _size_matched = 0

    def scan(self, dir: str) -> dict:
        if config.PROGRESS_BAR:
            status = progress.Bar(" Scanning", 40, 0)
        else:
            status = None
        self._tree_by_size = self._recurse_into_folder(dir, pb=status)
        if status:
            status.close()
        return self._tree_by_size

    def _recurse_into_folder(self, dir: str, by_size: dict = {}, pb: progress.Bar = None) -> dict:
        """find all files under current folder and group by size"""
        output(f"Searching in {dir}", Verbosity.Information)
        for entry in os.scandir(dir):
            if entry.is_file():
                ext = os.path.splitext(entry.name)[1][1:].lower()
                if config.valid_extension(ext):
                    size = os.path.getsize(entry.path)
                    if config.valid_size(size):
                        fd = File_Data(entry.name, entry.path, ext, size)
                        output(f"  {entry.path}: {size} bytes", Verbosity.Waffle)
                        if size not in by_size:
                            by_size[size] = []
                        by_size[size].append(fd)
                        if len(by_size[size]) > 2:
                            self._total_size += size
                            self._size_matched += 1
                        elif len(by_size[size]) == 2:
                            self._total_size += size * 2
                            self._size_matched += 2
                        self._files_found += 1
                        if pb:
                            pb.update(suffix=f"F = {self._files_found} | D = {self._size_matched}")
                    else:
                        output(f"  {entry.path}: {size} bytes discarded for size", Verbosity.Waffle)
                        self._files_rejected_size += 1
                else:
                    output(f"  {entry.path} discarded; not in category", Verbosity.Waffle)
                    self._files_rejected_cat += 1
            elif entry.is_dir():
                if entry.name[:1] == '.' and not config.INCLUDE_HIDDEN:
                    output(f"Skipping hidden folder {entry.path}", Verbosity.Detailed)
                elif entry.name == '.git':
                    output(f"Skipping hidden .git folder despite --hidden flag", Verbosity.Detailed)
                elif entry.name == config.ARCHIVE_FOLDER:
                    output(f"Skipping archive folder {entry.path}", Verbosity.Detailed)
                else:
                    self._recurse_into_folder(entry.path, by_size, pb)
        return by_size
