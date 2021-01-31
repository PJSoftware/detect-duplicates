import hashlib
import os

by_size = {}
by_hash = {}

def find():
    print("Find duplicates")
    dir = '.'
    recurse_into_folder(dir)
    for size in sorted(by_size.keys()):
        count = len(by_size[size])
        if count > 1:
            print(f"Files of size {size}: {count}")
            for file in by_size[size]:
                hash = hash_file(file)
                if not size in by_hash:
                    by_hash[size] = {}
                if not hash in by_hash[size]:
                    by_hash[size][hash] = {}
                print(f"  {file}: {hash}")

def move():
    print("Move duplicates")

def delete():
    print("Delete duplicates")

def recurse_into_folder(dir):
    print(f"Searching in {dir}")
    for entry in os.scandir(dir):
        if entry.is_file():
            size = os.path.getsize(entry.path)
            if size > 0:
                print(f"  {entry.path}: {size} bytes")
                if size not in by_size:
                    by_size[size] = []
                by_size[size].append(entry.path)
        elif entry.is_dir():
            if entry.name[:1] == '.':
                print(f"Skipping folder {entry.path}")
            # elif entry.name == '_dup_archive':
            #     print(f"Skipping archive folder {entry.path}")
            else:
                recurse_into_folder(entry.path)

def hash_file(file_path: str) -> str:
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(sha1.block_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
