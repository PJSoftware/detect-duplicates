import os
from typing import Optional

from .output import output
from . import config, progress, fingerprint
from .config import Verbosity

class File_Data():
    name = ''
    path = ''
    ext = ''
    size = 0
    
    _hash = ''

    def __init__(self, name: str, path: str, ext: str, size: int):
        self.name = name
        self.path = path
        self.ext = ext
        self.size = size

    @property
    def hash(self) -> str:
        self._hash = fingerprint.generate(self.path, self.size)
        return self._hash

    @hash.setter
    def hash(self, value):
        raise ValueError("hash must not be set manually; it is calculated internally")
    
class Folder_Data():
    _tree_by_size: dict = {}

    total_size = 0
    files_found = 0
    files_rejected_size = 0
    files_rejected_cat = 0
    size_matched = 0

    def __init__(self):
        self._scan('.')

    def data(self) -> dict:
        return self._tree_by_size

    def _scan(self, dir: str):
        status: Optional[progress.Bar]
        if config.PROGRESS_BAR:
            status = progress.Bar(" Scanning", 40, 0)
        else:
            status = None
        self._tree_by_size = self._recurse_into_folder(dir, pb=status)
        if status:
            status.close()

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
                            self.total_size += size
                            self.size_matched += 1
                        elif len(by_size[size]) == 2:
                            self.total_size += size * 2
                            self.size_matched += 2
                        self.files_found += 1
                        if pb:
                            pb.update(suffix=f"F = {self.files_found} | D = {self.size_matched}")
                    else:
                        output(f"  {entry.path}: {size} bytes discarded for size", Verbosity.Waffle)
                        self.files_rejected_size += 1
                else:
                    output(f"  {entry.path} discarded; not in category", Verbosity.Waffle)
                    self.files_rejected_cat += 1
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
