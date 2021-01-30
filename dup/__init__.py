import hashlib
import os

by_size = {}

def version():
    folder = os.path.abspath(os.path.dirname(__file__))
    with open(folder + '/VERSION') as f:
        version_data = f.read().splitlines()
        return version_data[0]
    
def usage():
    print(f"dup version {version()}")
    print("Find duplicate files within the current folder")
    print("Control flags are:")
    print("    -h  include hidden files/folders (excluded by default)*")
    print("    -z  include zero-length files (ignored by default)*")
    print("\n* not yet implemented")

def find():
    dir = '.'
    recurse_into_folder(dir)
    for size in sorted(by_size.keys()):
        count = len(by_size[size])
        if count > 1:
            print(f"Files of size {size}: {count}")
            for file in by_size[size]:
                hash = hash_file(file)
                print(f"  {file}: {hash}")

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
            else:
                recurse_into_folder(entry.path)

def hash_file(file_path: str) -> str:
    BUF_SIZE = 8388608 # 8Mb
    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
