from .config import Verbosity
from .output import output
from .scan import Folder_Data
from . import config, plural

import os
import tempfile

def list():
    output("List extensions", Verbosity.Required)
    extensions = scan_extensions()
    count = 0
    if config.ALL_EXTENSIONS:
        output("All extensions found:", Verbosity.Required)
    else:
        output("Top Ten extensions found: (use --all for complete list)", Verbosity.Required)

    ext_by_count = {}
    for ext in extensions:
        ext_by_count[extensions[ext]['count']] = ext

    for ext_count in sorted(ext_by_count.keys(), reverse=True):
        if config.ALL_EXTENSIONS or count < 10:
            output(f"> {ext_by_count[ext_count]}:\t{ext_count} files found", Verbosity.Required)
            count += 1
        else:
            break

def scan_extensions(find_ext: str = "") -> dict:
    files = Folder_Data(False)
    by_size = files.data()
    check_case_sensitivity()
    by_ext: dict = {}
    for size in by_size:
        for fd in by_size[size]:
            ext = fd.ext
            if config.IGNORE_CASE:
                ext = ext.lower()
            ## TODO: type of by_ext[ext] differs depending on parameter? Fix this!
            if ext != "":
                if ext not in by_ext:
                    by_ext[ext] = {}
                    by_ext[ext]['count'] = 0
                    by_ext[ext]['list'] = []
                if find_ext == "":
                    by_ext[ext]['count'] += 1
                else:
                    by_ext[ext]['list'].append(fd)
    return by_ext

def check_case_sensitivity():
    tmphandle, tmppath = tempfile.mkstemp()
    os.close(tmphandle)
    output(f"Temp file: {tmppath}", Verbosity.Waffle)
    if os.path.exists(tmppath.upper()):
        output("Operating system is NOT case sensitive; --ignore-case enabled", Verbosity.Waffle)
        config.IGNORE_CASE = True
    os.remove(tmppath)

def show(ext: str):
    if config.IGNORE_CASE:
        ext = ext.lower()
    output(f"Show extension {ext}", Verbosity.Required)
    by_ext = scan_extensions(ext)
    if ext in by_ext:
        count = len(by_ext[ext]['list'])
        output(f"{plural(count,'file')} with extension '{ext}':", Verbosity.Required)
        for file in by_ext[ext]['list']:
            output(f"> {file}", Verbosity.Required)
    else:
        output(f"extension '{ext}' not found")

def delete(ext: str):
    output(f"Delete extension {ext}", Verbosity.Required)
