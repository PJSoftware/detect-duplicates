import os
from typing import Optional

from .config import Verbosity
from .output import output
from . import config, progress, fingerprint
from . import plural

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
    _tree_by_hash: dict = {}

    total_size = 0
    files_found = 0
    files_rejected_size = 0
    files_rejected_cat = 0
    size_matched = 0

    duplicates_found = 0
    total_hashed_size = 0
    files_hashed = 0

    def __init__(self, calc_hashes: bool = True):
        self._scan('.')
        if calc_hashes:
            files_str = plural(self.files_found, "file")
            output(f"> {files_str} found", Verbosity.Information)
            output(f"> {self.size_matched} potential duplicates (same size files)", Verbosity.Information)
            self._calculate_hashes()

    def data(self) -> dict:
        return self._tree_by_size

    def hashes(self) -> dict:
        return self._tree_by_hash

    def _calculate_hashes(self):
        by_size = self.data()
        output("Calculating hashes of same-sized files", Verbosity.Required)
        status: progress.Bar = None
        if config.VERBOSITY_LEVEL == Verbosity.Required:
            status = progress.Bar("  Hashing", 40, self.total_size)
        self.duplicates_found = 0
        by_hash: dict = {}
        for size in sorted(by_size.keys()):
            count = len(by_size[size])
            if count > 1:
                output(f"Files of size {size}: {count}", Verbosity.Waffle)
                for fd in by_size[size]:
                    file_hash = fd.hash
                    self.files_hashed += 1
                    self.total_hashed_size += size
                    if status:
                        status.update(self.total_hashed_size, f"{self.files_hashed} of {self.size_matched}")
                    if not size in by_hash:
                        by_hash[size] = {}
                    if not file_hash in by_hash[size]:
                        by_hash[size][file_hash] = []

                    by_hash[size][file_hash].append(fd)
                    if len(by_hash[size][file_hash]) > 2:
                        self.duplicates_found += 1
                    elif len(by_hash[size][file_hash]) == 2:
                        self.duplicates_found += 2

                    output(f"{fd.path}: {file_hash}", Verbosity.Waffle)
        if status:
            status.close()
        self._tree_by_hash = by_hash

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
