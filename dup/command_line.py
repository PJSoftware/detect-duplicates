import argparse
import os
import sys

from .config import Verbosity
from . import output, version
from . import extensions, duplicates, config

def main():
    # dup.usage()
    parser = argparse.ArgumentParser(
        description=f"dup v{version()}: find duplicate files within the current folder", 
        epilog="* not yet implemented")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="increase output verbosity (up to 3 levels)")
    parser.add_argument("-z", "--zero", action="store_true", help="include zero-length files")
    parser.add_argument("-i", "--hidden", action="store_true", help="include hidden files/folders")
    parser.add_argument("-s", "--show", action="store_true", help="show intended actions without doing anything*")
    
    behave = parser.add_argument_group("behaviour")
    behave.add_argument("--find", action="store_true", help="report duplicates only (default)")
    behave.add_argument("--move", action="store_true", help="move duplicates into separate folder for review*")
    behave.add_argument("--delete", action="store_true", help="delete duplicates*")
    
    other = parser.add_argument_group("other")
    other.add_argument("--list-ext", action="store_true", help="list unique extensions in folder tree")
    other.add_argument("--del-ext", help="delete files with specified extensions (eg, --del-ext ABC,XXX)*")
    other.add_argument("-a", "--all", action="store_true", help="list all extensions (default is top 10 only)")

    arg = parser.parse_args()

    output(f"dup v{version()}")
    config.VERBOSITY_LEVEL = min(arg.verbose, Verbosity.Waffle)
    config.INCLUDE_HIDDEN = arg.hidden
    config.IGNORE_ZERO_LENGTH = not arg.zero
    config.ALL_EXTENSIONS = arg.all

    if arg.show:
        config.SHOW_DONT_ACT = True
        config.VERBOSITY_LEVEL = max(config.VERBOSITY_LEVEL, Verbosity.Detailed)
        output("* --show specified; no action will be taken (implies -vv)", Verbosity.Detailed)

    output(f"* verbosity level set to {config.VERBOSITY_LEVEL}", Verbosity.Detailed)
    
    if arg.zero:
        output("* --zero specified; zero-length files will be included in comparison", Verbosity.Detailed)
    
    if arg.hidden:
        output("* --hidden specified; hidden files and folders will be included", Verbosity.Detailed)
    
    # process extension commands first
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
