"""
CSC110 Project for Arihant Bapna, Zippy Kim and Nick Asante.

The main file to run our amazing project
"""
import sys


def main() -> int:
    """The main entry into the app"""
    from aggregation.aggregate import Aggregate
    agg = Aggregate("data")
    agg.initialize_all_files()
    return 0


if __name__ == '__main__':
    sys.exit(main())
