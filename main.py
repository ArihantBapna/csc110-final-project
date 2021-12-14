"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

The main file to run our amazing project
"""
# Copyright (c) 2021. Arihant Bapna, Hongzip Kim and Nick Macasaet  - All Rights Reserved|
# You may use this code under the terms of the MIT License for the simple fact that I was too lazy
# to write my own license. You should have received a copy of the license with this project,
# if not and for any other queries contact me at: a.bapna@mail.utoronto.ca
# This code is part of the CSC110F 2021 Final Project for the group consisting of Arihant Bapna,
# Hongzip Kim and Nick Macasaet
import os
import sys


def main() -> int:
    """The main entry into the app"""
    from aggregate import Aggregate
    from reading import Reading
    agg = Aggregate("data")
    agg.initialize_all_files()
    print("Finished data downloading")
    reader = Reading("data")
    reader.do_all_read()

    return 0


if __name__ == '__main__':
    os.system("pip3 install -r requirements.txt")
    sys.exit(main())
