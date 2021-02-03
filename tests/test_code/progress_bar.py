from dup import progress
import time

for i in progress.bar(range(15), "Computing: ", 40):
    time.sleep(0.1) # any calculation you need

# pb = progress.Bar("Computing", 40, 1000)
# for i in range(1000):
#     pb.update(i)
#     time.sleep(0.1) # any calculation you need