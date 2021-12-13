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
from reader import Reader


@dataclass
class Reading:
    """
    Read all the initialized files
    """
    working_dir: str

    def __init__(self, working_dir: str) -> None:
        self.working_dir = working_dir

        # Employment Data
        employment = Reader(self.working_dir, "/employment", "data.csv")
        employment.read_data()

        # Consumer Data
        cpi = Reader(self.working_dir, "/cpi", "data.csv")
        cpi.read_data()

        # Flights Data
        flights = Reader(self.working_dir, "/flights", "data.csv")
        flights.read_data()

        # GDP Data
        gdp = Reader(self.working_dir, "/gdp", "data.csv")
        gdp.read_data()

        # Retail Data
        retail = Reader(self.working_dir, "/retail", "data.csv")
        retail.read_data()

        # Covid Data
        covid = Reader(self.working_dir, "/covid", "ON.json")
        covid.read_data()


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["reader"]
    })
