import argparse
import os
import sys

import dup

def main():
    # dup.usage()
    parser = argparse.ArgumentParser()
    parser.parse_args()
    
    dup.find()
