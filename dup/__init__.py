from enum import IntEnum
import os

def version() -> str:
    """returns version information read from VERSION file"""
    folder = os.path.abspath(os.path.dirname(__file__))
    with open(folder + '/VERSION') as f:
        version_data = f.read().splitlines()
        return version_data[0]

def plural(num: int, noun: str, nouns: str = "") -> str:
    """pluralise a noun depending on number"""
    if nouns == "":
        nouns = noun + "s"
    if num == 1:
        nouns = noun
    return f"{num} {nouns}"
