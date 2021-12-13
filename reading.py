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
from process import Process
from reader import Reader


@dataclass
class Reading:
    """
    Read all the initialized files
    """
    working_dir: str

    def __init__(self, working_dir: str) -> None:
        self.working_dir = working_dir

        process = Process()

        # Employment Data
        employment = Reader(self.working_dir, "/employment", "data.csv")
        employment.read_data()
        process.set_data(employment.data_frame)
        employment.data_frame = process.process_employment_data()
        process.clear_data()

        # Consumer Data
        cpi = Reader(self.working_dir, "/cpi", "data.csv")
        cpi.read_data()
        process.set_data(cpi.data_frame)
        cpi.data_frame = process.process_cpi_data()
        process.clear_data()

        # GDP Data
        gdp = Reader(self.working_dir, "/gdp", "data.csv")
        gdp.read_data()
        process.set_data(gdp.data_frame)
        gdp.data_frame = process.process_gdp_data()
        process.clear_data()

        # Retail Data
        retail = self.do_read_file("/retail", "data.csv")
        process.set_data(retail.data_frame)
        retail.data_frame = process.process_retail_data()
        process.clear_data()

        # Covid Data
        covid = Reader(self.working_dir, "/covid", "ON.json")
        covid.read_data()
        process.set_data(covid.data_frame)
        covid.data_frame = process.process_covid_data()

        # Post Processing of Data
        valid = not covid.fail and not retail.fail and \
            not gdp.fail and not cpi.fail and not employment.fail
        process.done_processing(valid)

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


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['reader', 'process']
    })
