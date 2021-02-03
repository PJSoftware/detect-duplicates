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
    p_opt.add_argument("-z", "--zero", action="store_true", help="include zero-length files")
    p_opt.add_argument("-x", "--hidden", action="store_true", help="include hidden files/folders")
    p_opt.add_argument("-r", "--rehearse", action="store_true", help="show intended actions without doing anything*")

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
    config.IGNORE_ZERO_LENGTH = not arg.zero
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
    
    if arg.zero:
        output("* --zero specified; zero-length files will be included in comparison", Verbosity.Required)
    
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
