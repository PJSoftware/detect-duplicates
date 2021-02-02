import hashlib
import os

from . import recurse_into_folder, output, plural, foldername
from .config import Verbosity
from . import global_var

def find():
    output("Find duplicates", Verbosity.Required)
    by_hash = find_duplicates()
    report_duplicates(by_hash)

def move():
    print("Move duplicates")

def delete():
    print("Delete duplicates")

def find_duplicates() -> dict:
    output("Scanning current folder tree", Verbosity.Required)
    global_var.files_found = 0
    by_size = recurse_into_folder('.')
    files = plural(global_var.files_found, "file")
    output(f"> {files} found", Verbosity.Information)
    output(f"> {global_var.size_matched} potential duplicates (same size files)", Verbosity.Information)
    by_hash = calculate_hashes(by_size)
    return by_hash

def calculate_hashes(by_size: dict) -> dict:
    output("Calculating hashes of same-sized files", Verbosity.Required)
    global_var.duplicates_found = 0
    global_var.size_matched = 0
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
                    by_hash[size][file_hash] = []
                else:
                    global_var.duplicates_found += 1
                by_hash[size][file_hash].append(file)
                output(f"{foldername(file)}: {file_hash}", Verbosity.Waffle)
    return by_hash

def hash_file(file_path: str) -> str:
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(sha1.block_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def report_duplicates(by_hash: dict):
    dup = plural(global_var.duplicates_found, "duplicate file")
    output(f"> {dup} found", Verbosity.Required)
    by_count = {}
    for size in by_hash:
        output(f"size: {size}", Verbosity.Waffle)
        for hash in by_hash[size]:
            output(f"hash: {hash}", Verbosity.Waffle)
            count = len(by_hash[size][hash])
            output(f"count: {count}", Verbosity.Waffle)

            if count > 1:
                if not count in by_count:
                    by_count[count] = 0
                by_count[count] += 1
    for count in (sorted(by_count.keys(), reverse=True)):
        num = by_count[count]
        sets = plural(num, "set")
        output(f"> {sets} of files with {count} duplicates", Verbosity.Required)
