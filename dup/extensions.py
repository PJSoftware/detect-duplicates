from . import recurse_into_folder, output
from .config import Verbosity
from . import config, plural, foldername

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

    for ext in sorted(extensions, key=extensions.get, reverse=True):
        if config.ALL_EXTENSIONS or count <= 10:
            output(f"> {ext}:\t{extensions[ext]} files found", Verbosity.Required)
            count += 1
        else:
            break

def scan_extensions(find_ext: str = "") -> dict:
    by_size = recurse_into_folder('.')
    check_case_sensitivity()
    by_ext = {}
    for size in by_size:
        for file in by_size[size]:
            ext = os.path.splitext(file)[1][1:]
            if config.IGNORE_CASE:
                ext = ext.lower()
            if ext != "":
                if find_ext == "":
                    if ext not in by_ext:
                        by_ext[ext] = 0
                    by_ext[ext] += 1
                else:
                    if ext not in by_ext:
                        by_ext[ext] = []
                    by_ext[ext].append(file)
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
        count = len(by_ext[ext])
        output(f"{plural(count,'file')} with extension '{ext}':", Verbosity.Required)
        for file in by_ext[ext]:
            output(f"> {foldername(file)}", Verbosity.Required)
    else:
        output(f"extension '{ext}' not found")

def delete(ext: str):
    output(f"Delete extension {ext}", Verbosity.Required)
