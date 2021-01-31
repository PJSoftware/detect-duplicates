import hashlib
import os

from . import recurse_into_folder, output
from .config import Verbosity

def find():
    output("Find duplicates", Verbosity.Required)
    by_size = recurse_into_folder('.')
    by_hash = {}
    for size in sorted(by_size.keys()):
        count = len(by_size[size])
        if count > 1:
            output(f"Files of size {size}: {count}", Verbosity.Waffle)
            for file in by_size[size]:
                file_hash = hash_file(file)
                if not size in by_hash:
                    by_hash[size] = {}
                if not file_hash in by_hash[size]:
                    by_hash[size][file_hash] = {}
                output(f"  {file}: {file_hash}", Verbosity.Waffle)

def move():
    print("Move duplicates")

def delete():
    print("Delete duplicates")

def hash_file(file_path: str) -> str:
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(sha1.block_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
