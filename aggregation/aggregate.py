"""
CSC110 Project for Arihant Bapna, Hongzip Kim and Nicholas Macasaet.

Aggregates all the data for the project and loads it all up
"""
import os
from dataclasses import dataclass
from pathlib import Path

from colorama import Fore, init

from aggregation.abstraction.cube import Cube


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
