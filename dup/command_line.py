import argparse
import os
import sys

from dup import extensions, duplicates
from . import VERBOSITY_LEVEL, version

def main():
    # dup.usage()
    parser = argparse.ArgumentParser(
        description=f"dup v{version()}: find duplicate files within the current folder", 
        epilog="* not yet implemented")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="increase output verbosity (up to 3 levels)*")
    parser.add_argument("-z", "--zero", action="store_true", help="include zero-length files*")
    parser.add_argument("-i", "--hidden", action="store_true", help="include hidden files/folders*")
    
    behave = parser.add_argument_group("behaviour")
    behave.add_argument("--find", action="store_true", help="report duplicates only (default)*")
    behave.add_argument("--move", action="store_true", help="move duplicates into separate folder for review*")
    behave.add_argument("--delete", action="store_true", help="delete duplicates*")
    
    other = parser.add_argument_group("other")
    other.add_argument("--list-ext", action="store_true", help="list unique extensions in folder tree*")
    other.add_argument("--del-ext", help="delete files with specified extension*")

    arg = parser.parse_args()

    global VERBOSITY_LEVEL
    VERBOSITY_LEVEL = min(arg.verbose, 3)

    if arg.del_ext:
        extensions.delete(arg.del_ext)
    elif arg.list_ext:
        extensions.list()

    elif arg.delete:
        duplicates.delete()
    elif arg.move:
        duplicates.move()
    else: # arg.find is the default
        duplicates.find()
