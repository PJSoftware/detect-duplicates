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

    p_act = parser.add_argument_group("actions")
    p_act.add_argument("--find", action="store_true", help="report duplicates only (default)")
    p_act.add_argument("--move", action="store_true", help="move duplicates into separate folder for review*")
    p_act.add_argument("--delete", action="store_true", help="delete duplicates*")

    p_ext = parser.add_argument_group("extensions")
    p_ext.add_argument("--list-ext", action="store_true", help="list unique extensions in folder tree")
    p_ext.add_argument("-a", "--all", action="store_true", help="list all extensions (default is top 10 only)")
    p_ext.add_argument("--show-ext", help="list files with specified extension (eg, --show-ext JPG)")
    p_ext.add_argument("--del-ext", help="delete files with specified extension (eg, --del-ext MD)*")
    p_ext.add_argument("-i", "--ignore-case", action="store_true", help="ignore case when specifying extension")

    p_opt = parser.add_argument_group("options")
    p_opt.add_argument("-x", "--hidden", action="store_true", help="include hidden files/folders")
    p_opt.add_argument("-r", "--rehearse", action="store_true", help="show intended actions without doing anything*")

    p_flt = parser.add_argument_group("filters")
    p_flt.add_argument("--min-size", help="min file size to consider (eg, --show-ext 4M) (default 1K)")
    p_flt.add_argument("--max-size", help="max file size to consider (eg, --show-ext 40M)")

    p_stat = parser.add_argument_group("status")
    p_stat.add_argument("-p", "--progress", action="store_true", help="display progress bar (default)*")
    p_stat.add_argument(
        "-v", "--verbose", action="count", default=Verbosity.Required, 
        help="increase output verbosity, up to 3 levels (disables --progress)")

    arg = parser.parse_args()

    output(f"dup v{version()}")
    config.PROGRESS_BAR = True
    config.VERBOSITY_LEVEL = min(arg.verbose, Verbosity.Waffle)
    config.INCLUDE_HIDDEN = arg.hidden
    config.ALL_EXTENSIONS = arg.all
    config.IGNORE_CASE = arg.ignore_case

    if arg.rehearse:
        config.SHOW_DONT_ACT = True
        config.VERBOSITY_LEVEL = max(config.VERBOSITY_LEVEL, Verbosity.Detailed)
        output("* --rehearse specified; no action will be taken (implies -vv)", Verbosity.Required)

    if config.VERBOSITY_LEVEL > Verbosity.Required:
        config.PROGRESS_BAR = False
        output(f"* verbosity level set to {config.VERBOSITY_LEVEL}", Verbosity.Detailed)
        output("* progress bar has been disabled", Verbosity.Detailed)
    
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
        output("* --hidden specified; hidden files and folders will be included", Verbosity.Required)
    
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
