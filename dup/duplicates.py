import hashlib
import ntpath
import os
import re
import shutil

from . import plural
from .config import Verbosity
from .output import output, cleanse_output
from .scan import Folder_Data
from . import global_var, config, progress, fingerprint

def find():
    output("Find duplicates", Verbosity.Required)
    files = find_duplicates()
    report_duplicates(files)

def archive():
    output("Archive duplicates", Verbosity.Required)
    files = find_duplicates()
    archive_duplicates(files)

def delete():
    output("Delete duplicates", Verbosity.Required)

def find_duplicates() -> Folder_Data:
    output("Scanning current folder tree    F=found | D=possible duplicates", Verbosity.Required)
    files = Folder_Data()
    return files

def report_duplicates(files: Folder_Data):
    by_hash = files.hashes()
    dup = plural(global_var.duplicates_found, "duplicate file")
    acc_range = f"{config.MIN_SIZE}"
    if config.MAX_SIZE < config.MIN_SIZE:
        acc_range += " and above"
    elif config.MAX_SIZE == config.MIN_SIZE:
        acc_range += " exactly"
    else:
        acc_range += f" to {config.MAX_SIZE}"
    num_files = plural(files.files_rejected_cat + files.files_rejected_size, "file")
    output(f"> {num_files} skipped for size ({acc_range}) or category", Verbosity.Required)
    output(f"> {dup} found", Verbosity.Required)
    if config.VERBOSITY_LEVEL == Verbosity.Required:
        by_count: dict = {}
        for size in by_hash:
            output(f"size: {size}", Verbosity.Waffle)
            for hash in by_hash[size]:
                output(f"hash: {hash}", Verbosity.Waffle)
                count = len(by_hash[size][hash])
                output(f"count: {count}", Verbosity.Waffle)

                if count > 1:
                    if not count in by_count:
                        by_count[count] = {}
                    if not size in by_count[count]:
                        by_count[count][size] = []
                    by_count[count][size] = by_hash[size][hash]

        for count in (sorted(by_count.keys(), reverse=True)):
            num_sets = 0
            min_size = -1
            max_size = -1
            for size in (sorted(by_count[count])):
                num_sets += 1
                if min_size == -1:
                    min_size = size
                max_size = max(max_size, size)
            sets = plural(num_sets, "set")
            size_range = f"{min_size} bytes"
            if max_size > min_size:
                size_range += f" to {max_size} bytes"
            output(f"> {sets} of files with {count} duplicates ({size_range})", Verbosity.Required)
    else:
        for size in (sorted(by_hash.keys())):
            for hash in by_hash[size]:
                count = len(by_hash[size][hash])
                if count > 1:
                    output(f"> {size}-byte files with {count} duplicates", Verbosity.Required)
                    for file in (sorted(by_hash[size][hash])):
                        output(f"> {file}", Verbosity.Information)

def archive_duplicates(files: Folder_Data):
    by_hash = files.hashes()
    output("Archiving duplicates", Verbosity.Required)
    if config.VERBOSITY_LEVEL == Verbosity.Required:
        status = progress.Bar("Archiving", 40, global_var.duplicates_found)
    else:
        status = None

    archived = 0
    for size in by_hash:
        for hash in by_hash[size]:
            index = determine_preferred_master(by_hash[size][hash])
            count = len(by_hash[size][hash])
            
            if count < 2:
                break

            archive_folder = f"{config.ARCHIVE_FOLDER}/{size}-{hash[:6]}-{count}"
            os.makedirs(archive_folder, exist_ok=True)

            copy_to(archive_folder, by_hash[size][hash][index])
            archived += 1
            if status:
                status.update(archived, f"{archived} of {global_var.duplicates_found}")
            j = 1
            for i in range(count):
                if i != index:
                    move_to(archive_folder, by_hash[size][hash][i], j)
                    j += 1
                    archived += 1
                    if status:
                        status.update(archived, f"{archived} of {global_var.duplicates_found}")
    
    if status:
        status.close()

def determine_preferred_master(files: list) -> int:
    for i, file_path in enumerate(files):
        if not re.search("unsorted|copy", file_path, re.IGNORECASE):
            return i
    return 0

def copy_to(folder: str, file_path: str):
    output(f"Copying {file_path} to {folder}", Verbosity.Detailed)
    if config.SHOW_DONT_ACT:
        return
    fn = ntpath.basename(file_path)
    tfn = f"0-{fn}"
    archive_log(folder, file_path, tfn, 'copied')
    shutil.copy2(file_path,f"{folder}/{tfn}")
            
def move_to(folder: str, file_path: str, num: int):
    output(f"#{num}: Moving {file_path} to {folder}", Verbosity.Detailed)
    if config.SHOW_DONT_ACT:
        return
    fn = ntpath.basename(file_path)
    tfn = f"{num}-{fn}"
    archive_log(folder, file_path, tfn, 'moved')
    shutil.move(file_path,f"{folder}/{tfn}")

def archive_log(folder: str, source: str, target: str, action: str):
    log_file = f"{folder}/archive.log"
    with open(log_file, 'a') as f:
        f.write(cleanse_output(f"[{target}] {action} from [{source}]\n"))
