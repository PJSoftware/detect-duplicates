from . import recurse_into_folder, output
from .config import Verbosity

import os
import tempfile

def list():
    output("List extensions", Verbosity.Required)
    extensions = scan_extensions()
    for ext in sorted(extensions, key=extensions.get, reverse=True):
        output(f"> {ext}: {extensions[ext]} files found", Verbosity.Required)

def scan_extensions() -> dict:
    by_size = recurse_into_folder('.')
    cs = is_os_case_sensitive()
    by_ext = {}
    for size in by_size:
        for file in by_size[size]:
            ext = os.path.splitext(file)[1][1:]
            if not cs:
                ext = ext.lower()
            if ext != "":
                if ext not in by_ext:
                    by_ext[ext] = 0
                by_ext[ext] += 1
    return by_ext

def is_os_case_sensitive() -> bool:
    tmphandle, tmppath = tempfile.mkstemp()
    os.close(tmphandle)
    output(f"Temp file: {tmppath}", Verbosity.Waffle)
    if os.path.exists(tmppath.upper()):
        output("Operating system is NOT case sensitive", Verbosity.Waffle)
        cs = False
    else:
        output("Operating system is case sensitive", Verbosity.Waffle)
        cs = True
    os.remove(tmppath)
    return cs

def delete(ext: str):
    output(f"Delete extension {ext}", Verbosity.Required)
