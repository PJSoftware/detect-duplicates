# Found at https://stackoverflow.com/questions/3160699/python-progress-bar/34482761#34482761
#
# Usage:
#
# import time
#
# for i in progressbar(range(15), "Computing: ", 40):
#     time.sleep(0.1) # any calculation you need

import sys

def bar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
