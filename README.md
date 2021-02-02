# detect-duplicates

```text
usage: dup [-h] [-v] [-z] [-i] [-s] [--find] [--move] [--delete] [--list-ext]
           [--del-ext DEL_EXT]

dup v0.0.2: find duplicate files within the current folder

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      increase output verbosity (up to 3 levels)*
  -z, --zero         include zero-length files*
  -i, --hidden       include hidden files/folders*
  -s, --show         show intended actions without doing anything*

behaviour:
  --find             report duplicates only (default)*
  --move             move duplicates into separate folder for review*
  --delete           delete duplicates*

other:
  --list-ext         list unique extensions in folder tree*
  --del-ext DEL_EXT  delete files with specified extensions (eg, --del-ext
                     ABC,XXX)*

* not yet implemented
```
