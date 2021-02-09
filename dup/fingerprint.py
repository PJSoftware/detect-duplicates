import hashlib
import os

from . import global_var, Verbosity
from .output import cleanse_output, output

cache_file = ".dup_fingerprint.cache"
cache_imported = False
cache_data = {}

def generate(file_path: str, size: int) -> str:
    if not cache_imported:
        import_cache()
    
    fp = find_in_cache(file_path, size)
    if fp != "":
        output(f"{file_path} hash imported: {fp}", Verbosity.Information)
        global_var.files_hashed += 1
        return fp

    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(sha1.block_size)
            if not data:
                break
            sha1.update(data)
    fp = sha1.hexdigest()
    output(f"{file_path} hash calculated: {fp}", Verbosity.Information)
    export_to_cache(file_path, size, fp)
    global_var.files_hashed += 1
    return fp

def import_cache():
    global cache_imported, cache_data
    cache_imported = True
    if not os.path.isfile(cache_file):
        return

    cache = open(cache_file, 'r')
    for line in cache:
        line = line.strip()
        fp, size, file_path = line.split('|', 2)
        cache_data[file_path] = {}
        cache_data[file_path]["size"] = int(size)
        cache_data[file_path]["fp"] = fp
    cache.close()
    os.remove(cache_file)

def find_in_cache(file_path: str, size: int) -> str:
    file_path = cleanse_output(file_path)
    if file_path not in cache_data:
        return ""
    if cache_data[file_path]["size"] == size:
        fp = cache_data[file_path]["fp"]
        export_to_cache(file_path, size, fp)
        return fp
    return ""

def export_to_cache(file_path: str, size: int, fp: str):
    cache = open(cache_file, 'a+')
    file_path = cleanse_output(file_path)
    cache.write(f"{fp}|{size}|{file_path}\n")
    cache.close()
