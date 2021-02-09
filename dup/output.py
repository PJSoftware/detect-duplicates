import platform

from . import config

def output(string: str, level: int = config.Verbosity.Required):
    """print string if specified level allowed by VERBOSITY settings"""
    if level <= config.VERBOSITY_LEVEL:
        print("  "*level + cleanse_output(string))

def cleanse_output(fn: str) -> str:
    """workaround for dodgy file/folder names which break Python"""
    if platform.system() == "Windows":
        return fn.encode("utf-8").decode("cp1252","backslashreplace")
    return fn
