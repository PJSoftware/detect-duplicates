import sys, os
import time

# The linter cannot interpret this, se we need to disable following error
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# pylint: disable=no-name-in-module
from dup.progress import Bar
# pylint: enable=no-name-in-module

length = 175
pb1 = Bar("Computing", 40, length)
for i in range(length+1):
    pb1.update(i, f"Step {i}")
    time.sleep(0.1) # any calculation you need
print()

pb2 = Bar("Scanning", 40, 0)
for i in range(length+1):
    pb2.update(0, f"Step {i}")
    time.sleep(0.1) # any calculation you need
print()
