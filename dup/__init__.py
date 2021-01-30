import os

def version():
    folder = os.path.abspath(os.path.dirname(__file__))
    with open(folder + '/VERSION') as f:
        version_data = f.read().splitlines()
        return version_data[0]
    
def usage():
    print(f"dup version {version()}")
    print("Find duplicate files within the current folder")
    