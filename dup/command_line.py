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
        epilog="* not yet implemented; size can be expressed in bytes, or K, M, or G (eg, 10M)")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="increase output verbosity (up to 3 levels)")
    parser.add_argument("-x", "--hidden", action="store_true", help="include hidden files/folders")
    parser.add_argument("-r", "--rehearse", action="store_true", help="show intended actions without doing anything*")
    
    behave = parser.add_argument_group("behaviour")
    behave.add_argument("--find", action="store_true", help="report duplicates only (default)")
    behave.add_argument("--move", action="store_true", help="move duplicates into separate folder for review*")
    behave.add_argument("--delete", action="store_true", help="delete duplicates*")

    filter = parser.add_argument_group("filter")
    filter.add_argument("--min-size", help="min file size to consider (eg, --show-ext 4M) (default 1K)")
    filter.add_argument("--max-size", help="max file size to consider (eg, --show-ext 40M)")
    filter.add_argument("--category", help="file category to compare (eg, movies, images, docs)*")

    other = parser.add_argument_group("extensions")
    other.add_argument("--list-ext", action="store_true", help="list unique extensions in folder tree")
    other.add_argument("-a", "--all", action="store_true", help="list all extensions (default is top 10 only)")
    other.add_argument("--show-ext", help="list files by extension (eg, --show-ext JPG)")
    other.add_argument("--del-ext", help="delete files by extension (eg, --del-ext MD)*")
    other.add_argument("-i", "--ignore-case", action="store_true", help="ignore case when specifying extension")

    arg = parser.parse_args()

    output(f"dup v{version()}")
    config.VERBOSITY_LEVEL = min(arg.verbose, Verbosity.Waffle)
    config.INCLUDE_HIDDEN = arg.hidden
    config.ALL_EXTENSIONS = arg.all
    config.IGNORE_CASE = arg.ignore_case

    if arg.rehearse:
        config.SHOW_DONT_ACT = True
        config.VERBOSITY_LEVEL = max(config.VERBOSITY_LEVEL, Verbosity.Detailed)
        output("* --show specified; no action will be taken (implies -vv)", Verbosity.Detailed)

    output(f"* verbosity level set to {config.VERBOSITY_LEVEL}", Verbosity.Detailed)

    if arg.min_size:
        config.MIN_SIZE = config.calc_file_size(arg.min_size)
        if config.MIN_SIZE == -1:
            config.MIN_SIZE = config.calc_file_size("1K")
            output(f"* --min-size {arg.min_size} not recognised: set to default value {config.MIN_SIZE}", Verbosity.Required)
        else:
            output(f"* --min-size set to {config.MIN_SIZE} bytes", Verbosity.Detailed)
    else:
        config.MIN_SIZE = config.calc_file_size("1K")

    if arg.max_size:
        config.MAX_SIZE = config.calc_file_size(arg.max_size)
        if config.MAX_SIZE == -1:
            output(f"* --max-size {arg.max_size} not recognised: set to default of no limit", Verbosity.Required)
        else:
            if config.MAX_SIZE < config.MIN_SIZE:
                output(f"* --max-size {config.MAX_SIZE} smaller than --min_size; setting to {config.MIN_SIZE}", Verbosity.Required)
                config.MAX_SIZE = config.MIN_SIZE
            output(f"* --max-size set to {config.MIN_SIZE} bytes", Verbosity.Detailed)

    if arg.hidden:
        output("* --hidden specified; hidden files and folders will be included", Verbosity.Detailed)
    
    # process extension commands first
    if arg.del_ext:
        extensions.delete(arg.del_ext)
    elif arg.show_ext:
        extensions.show(arg.show_ext)
    elif arg.list_ext:
        extensions.list()

    elif arg.delete:
        duplicates.delete()
    elif arg.move:
        duplicates.move()
    else: # arg.find is the default
        duplicates.find()
