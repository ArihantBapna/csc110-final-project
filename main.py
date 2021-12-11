"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

The main file to run our amazing project
"""
import os
import sys


def main() -> int:
    """The main entry into the app"""
    from compilation.aggregate import Aggregate
    agg = Aggregate("data")
    agg.initialize_all_files()
    return 0


if __name__ == '__main__':
    os.system("pip3 install -r requirements.txt")
    sys.exit(main())
