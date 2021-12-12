"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Aggregates all the data for the project and loads it all up
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet

import os
from dataclasses import dataclass
from pathlib import Path

from colorama import Fore, init

from cube import Cube
from openvcovid import OpenCovid
from reader import Reader


@dataclass
class Aggregate:
    """
    Responsible for all data validity across program start
    """
    working_dir: str

    def __init__(self, working_dir: str) -> None:
        init(autoreset=True)
        # Set the working directory for all the data
        self.working_dir = working_dir
        # Check if the data working directory exists and create it if not
        work_dir = Path(self.working_dir)
        if work_dir.is_dir():
            print("[INFO]: Found the data source at " + str(work_dir.absolute())
                  + ". Attempting to read data.")
        else:
            print(Fore.YELLOW + "[WARNING]: Could not find " + str(work_dir.absolute())
                  + ". Attempting to create one")
            try:
                os.mkdir(Path(self.working_dir))
            except OSError as error:
                print(Fore.RED + "[FATAL ERROR]: Unable to create " + str(work_dir.absolute())
                      + str(error) + ". Ensure adequate permissions.")
                exit(1)  # exit marked here if unable to create/find the working directory
            else:
                print("[INFO]: Successfully created " + str(work_dir.absolute())
                      + " as the data directory")

    def initialize_all_files(self) -> None:
        """
        Initializes all the data files
        """
        self.initialize_gdp_file()
        self.initialize_cpi_file()
        self.initialize_employment_file()
        self.initialize_retail_file()
        self.initialize_flights_file()
        self.initialize_covid_file()

        # Employment Data
        employment = Reader(self.working_dir, "/employment")
        employment.read_data()

        # Consumer Data
        cpi = Reader(self.working_dir, "/cpi")
        cpi.read_data()

        # Flights Data
        flights = Reader(self.working_dir, "/flights")
        flights.read_data()

        # GDP Data
        gdp = Reader(self.working_dir, "/gdp")
        gdp.read_data()

        # Retail Data
        retail = Reader(self.working_dir, "/retail")
        retail.read_data()

        # Covid Data
        covid = Reader(self.working_dir, "/covid")
        covid.read_data()

    def initialize_gdp_file(self) -> None:
        """
        - Statistics Canada -
        Gross domestic product (GDP) at basic prices, by industry, monthly (x 1,000,000)
        Link: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610043401
        """
        Cube(36100434, self.working_dir + "/gdp")

    def initialize_cpi_file(self) -> None:
        """
        - Statistics Canada -
        Consumer Price Index, monthly, not seasonally adjusted
        Link: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000401
        """
        Cube(18100004, self.working_dir + "/cpi")

    def initialize_employment_file(self) -> None:
        """
        - Statistics Canada -
        Labour force characteristics by province, monthly, seasonally adjusted
        Link: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028703
        """
        Cube(14100287, self.working_dir + "/employment")

    def initialize_retail_file(self) -> None:
        """
        - Statistics Canada -
        Retail trade sales by province and territory (x 1,000)
        Link: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010000801
        """
        Cube(20100008, self.working_dir + "/retail")

    def initialize_flights_file(self) -> None:
        """
        - Statistics Canada -
        Domestic and international Itinerant movements, by type of operation,
        airports with NAV CANADA towers, monthly
        Link: https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=2310000801
        """
        Cube(23100008, self.working_dir + "/flights")

    def initialize_covid_file(self) -> None:
        """
        - OpenCovid Canada -
        Open Source Covid Cases Data
        Link: https://opencovid.ca/api/
        """
        OpenCovid("ON", self.working_dir + "/covid")
