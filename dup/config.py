from enum import IntEnum
import re

class Verbosity(IntEnum):
    Required = 0
    Information = 1
    Detailed = 2
    Waffle = 3

VERBOSITY_LEVEL = Verbosity.Required
INCLUDE_HIDDEN = False
SHOW_DONT_ACT = False
ALL_EXTENSIONS = False
IGNORE_CASE = False
PROGRESS_BAR = True
MIN_SIZE = -1
MAX_SIZE = -1

ARCHIVE_FOLDER = '_dup_archive_'

def calc_file_size(size:str) -> int:
    mult_table = {"T":1024**4, "G":1024**3, "M":1024**2, "K":1024}
    keys = "".join(mult_table.keys())
    found = re.match(r"^(\d+)(["+keys+"]?)$", size, re.IGNORECASE)
    if found:
        base = int(found[1])
        if found[2] == "":
            mult = 1
        else:
            mult = mult_table[found[2].upper()]
        return base * mult
    return -1

def valid_size(size:int) -> bool:
    if size < MIN_SIZE:
        return False
    if MAX_SIZE >= MIN_SIZE and size > MAX_SIZE:
        return False
    return True
