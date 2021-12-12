"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Abstract Reader file that loads all the csv files into
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from colorama import deinit, Fore, init
from tqdm import tqdm

from aggregate import Aggregate


@dataclass
class Reader(Aggregate):
    """
    Abstract class to read csv files
    """
    local_dir: str
    file_path: str
    data_frame: pd.DataFrame
    fail: bool

    def __init__(self, working_dir: str, local_dir: str):
        super().__init__(working_dir)
        self.local_dir = local_dir

        filename = working_dir + local_dir + "/data.csv"
        self.file_path = filename

        self.fail = False

    def read_data(self) -> None:
        """
        Reads the csv file associated with the aggregate reader
        """
        init(autoreset=True)

        print("[INFO]: Opening file " + self.file_path)

        try:
            with open(self.file_path) as f:
                total_len = sum(1 for _ in f)
        except IOError as error:
            print(
                Fore.RED + "[FATAL ERROR]: Could not find data file " + self.file_path + " in " +
                self.local_dir)
            print(str(error))
            self.fail = True
            return
        else:
            print(
                "[INFO]: Confirmed " + str(total_len) + " lines to be read from " + self.file_path)

        try:
            if '.csv' in self.file_path:
                data = self.chunk_reading_csv(total_len, max([total_len // 10, 1000000]))
            else:
                data = self.chunk_reading_json(total_len, max([total_len // 10, 1000000]))
        except IOError:
            print(Fore.RED + "[FATAL ERROR]: IO Error when reading " + str(
                Path(self.file_path).absolute()) + ". ")
            self.fail = True
            return
        else:
            print(Fore.GREEN + "[SUCCESS]: Done reading " + str(Path(self.file_path).absolute()))
            print("[INFO]: Pandas dataframe contains " + str(
                data.size) + " data points shaped " + str(data.shape))
            print("[DATA]: ")
            print(data.head(5))

        deinit()

    def start_reading(self) -> pd.DataFrame:
        """
        Creates a progress bar to read
        :return:
        """
        temp = pd.read_csv(self.file_path, nrows=20)
        n = len(temp.to_csv(index=False))
        df = [temp[:0]]
        t = int(os.path.getsize(self.file_path) / n * 20 / 10 ** 5) + 1
        with tqdm(total=t, file=sys.stdout) as pbar:
            for i, chunk in enumerate(
                    pd.read_csv(self.file_path, chunksize=10 ** 5, low_memory=False)):
                df.append(chunk)
                pbar.set_description('[INFO] Reading: %d' % (1 + i))
                pbar.update(1)

        data = temp[:0].append(df)
        del df

        return data

    def chunk_reading_csv(self, length: int, chunksize: int):
        """
        Read the given data file through chunking
        :param chunksize:
        :param length:
        """
        chunksize = chunksize

        data = pd.DataFrame()

        with tqdm(total=length, file=sys.stdout) as pbar:
            for chunk in pd.read_csv(self.file_path, chunksize=chunksize, low_memory=False):
                pbar.update(chunksize)
                if data is pd.DataFrame():
                    data = chunk
                else:
                    data = data.append(chunk)

        return data

    def chunk_reading_json(self, length: int, chunksize: int):
        """
        Read the given json data file through chunking
        :param length:
        :param chunksize:
        :return:
        """
        chunksize = chunksize

        data = pd.DataFrame()

        with tqdm(total=length, file=sys.stdout) as pbar:
            for chunk in pd.read_json(self.file_path, chunksize=chunksize, low_memory=False):
                pbar.update(chunksize)
                if data is pd.DataFrame():
                    data = chunk
                else:
                    data = data.append(chunk)

        return data
