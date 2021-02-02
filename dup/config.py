from enum import IntEnum

class Verbosity(IntEnum):
    Required = 0
    Information = 1
    Detailed = 2
    Waffle = 3

VERBOSITY_LEVEL = Verbosity.Required
INCLUDE_HIDDEN = False
IGNORE_ZERO_LENGTH = True
SHOW_DONT_ACT = False
ALL_EXTENSIONS = False

ARCHIVE_FOLDER = '_dup_archive_'
