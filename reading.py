"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Class that actually does the reading for the project
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet

from dataclasses import dataclass
import multiprocessing as mp
from pathlib import Path

import pandas as pd
from colorama import Fore

from writing import Writing
from process import Process
from reader import Reader


@dataclass
class Reading:
    """
    Read all the initialized files
    """
    working_dir: str
    process: Process
    writing: Writing

    def __init__(self, working_dir: str, write: Writing) -> None:
        self.working_dir = working_dir
        self.process = Process()
        self.writing = write

    def do_all_read(self) -> None:
        """
        Read all the files and initialize for processed data
        :return:
        """

        # Employment Data
        employment_process = mp.Process(target=self.employment_read, args=())
        employment_process.start()
        employment_process.join()

        # Consumer Data
        cpi_process = mp.Process(target=self.cpi_read, args=())
        cpi_process.start()
        cpi_process.join()

        # GDP Data
        gdp_process = mp.Process(target=self.gdp_read, args=())
        gdp_process.start()
        gdp_process.join()

        # Retail Data
        retail_process = mp.Process(target=self.retail_read, args=())
        retail_process.start()
        retail_process.join()

        # Covid Data
        covid_process = mp.Process(target=self.covid_read, args=())
        covid_process.start()
        covid_process.join()

    def do_all_processed_read(self) -> tuple:
        """
        Read all the processed datasets
        """
        employment = self.processed_reader('employment.csv')
        cpi = self.processed_reader('cpi.csv')
        gdp = self.processed_reader('gdp.csv')
        retail = self.processed_reader('retail.csv')
        covid = self.processed_reader('covid.csv')

        return (employment, cpi, gdp, retail, covid)

    def employment_read(self) -> None:
        """
        Read the employment data file
        """

        employment = Reader(self.working_dir, "/employment", "data.csv")
        employment.read_data()
        self.process.set_data(employment.data_frame)
        employment.data_frame = self.process.process_employment_data()

        # Save the employment data to processed file
        self.writing.save_csv_data(employment.data_frame, "employment.csv")

    def cpi_read(self) -> None:
        """
        Read the cpi data file
        """

        cpi = Reader(self.working_dir, "/cpi", "data.csv")
        cpi.read_data()
        self.process.set_data(cpi.data_frame)
        cpi.data_frame = self.process.process_cpi_data()

        self.writing.save_csv_data(cpi.data_frame, "cpi.csv")

    def gdp_read(self) -> None:
        """
        Read the gdp data file
        """

        gdp = Reader(self.working_dir, "/gdp", "data.csv")
        gdp.read_data()
        self.process.set_data(gdp.data_frame)
        gdp.data_frame = self.process.process_gdp_data()

        self.writing.save_csv_data(gdp.data_frame, "gdp.csv")

    def retail_read(self) -> None:
        """
        Read the retail data file
        """

        retail = self.do_read_file("/retail", "data.csv")
        self.process.set_data(retail.data_frame)
        retail.data_frame = self.process.process_retail_data()

        self.writing.save_csv_data(retail.data_frame, "retail.csv")

    def covid_read(self) -> None:
        """
        Read the covid data file
        """

        covid = Reader(self.working_dir, "/covid", "ON.json")
        covid.read_data()
        self.process.set_data(covid.data_frame)
        covid.data_frame = self.process.process_covid_data()

        self.writing.save_csv_data(covid.data_frame, "covid.csv")

    def do_read_file(self, local_dir: str, filename: str) -> Reader:
        """
        Create a reader object, read and process the data
        :param local_dir:
        :param filename:
        :return:
        """
        reader_object = Reader(self.working_dir, local_dir, filename)
        reader_object.read_data()
        return reader_object

    def processed_reader(self, filename: str) -> pd.DataFrame:
        """
        Read the processed data file
        """

        reader = Reader(self.working_dir, "/processed_data", filename)
        reader.read_data()

        if reader.fail:
            print(Fore.RED + "[FATAL ERROR]: Could not read " + filename
                  + " from processed data folder. Folder may be corrupted. Delete it and run again")
            exit(1)
        else:
            print(Fore.GREEN + "[SUCCESS]: Read " + str(Path(self.working_dir, "/processed_data",
                                                             filename).absolute()) + " into memory")
            reader.data_frame['Date'] = pd.to_datetime(reader.data_frame['Date'], errors='coerce')
            print(Fore.BLUE + "[DATA] PROCESSED: ")
            print(reader.data_frame.head(5))

        return reader.data_frame


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['reader', 'process', 'writing']
    })
