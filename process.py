"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Class that processes all the data for the project

Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
of the MIT License. You should have received a copy of the license with this project,
if not and for any other queries contact me at: a.bapna@mail.utoronto.ca This code is part of the
CSC110F 2021 Final Project for the group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
"""

import gc
from dataclasses import dataclass
import pandas as pd
from colorama import deinit, Fore, init


@dataclass
class Process:
    """
    Data Processing File
    """
    data: pd.DataFrame

    def __init__(self) -> None:
        print("[INFO]: Initializing data processing")

    def set_data(self, data: pd.DataFrame) -> None:
        """
        Set the data for processing
        :param data:
        """
        self.data = data

    def clear_data(self) -> None:
        """
        Clear the data for the file and collect the garbage
        :return:
        """
        print(Fore.MAGENTA + "[Memory]: Clearing up the memory for processing")
        self.data = pd.DataFrame()
        gc.collect()

    def process_employment_data(self) -> pd.DataFrame:
        """
        Process the employment dataframe
        """
        init(autoreset=True)

        self.data = self.data[(self.data['GEO'] == "Ontario")
                              & (self.data['Labour force characteristics'] == "Unemployment rate")
                              & (self.data['Statistics'] == 'Estimate')
                              & (self.data['Data type'] == "Seasonally adjusted")]

        self.data = self.data.drop(['GEO', 'DGUID', 'Labour force characteristics', 'Statistics',
                                    'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR',
                                    'COORDINATE', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS',
                                    'Data type'],
                                   axis=1)
        self.data = self.data.rename(columns={'REF_DATE': 'Date', 'VALUE': 'UnemploymentValue',
                                              'Age group': 'Age'})
        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

        self.display_data()

        return self.data

    def process_cpi_data(self) -> pd.DataFrame:
        """
        Process the consumer price index dataframe
        """
        init(autoreset=True)

        self.data = self.data[(self.data['GEO'] == "Ontario")
                              & (self.data['Products and product groups'] == "All-items")]

        self.data = self.data.drop(['GEO', 'DGUID', 'Products and product groups',
                                    'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR',
                                    'COORDINATE', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS'],
                                   axis=1)
        self.data = self.data.rename(columns={'REF_DATE': 'Date', 'VALUE': 'CpiValue'})

        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

        self.display_data()

        return self.data

    def process_gdp_data(self) -> pd.DataFrame:
        """
        Process gdp contribution data of Retail trade
        """
        init(autoreset=True)

        self.data = self.data[(self.data['Prices'] == "Chained (2012) dollars")
                              & (self.data['North American Industry Classification '
                                           'System (NAICS)'] == "Retail trade ["
                                                                "44-45]")]

        self.data = self.data.drop(['GEO', 'DGUID', 'Seasonal adjustment', 'UOM', 'UOM_ID',
                                    'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE', 'STATUS',
                                    'SYMBOL', 'TERMINATED', 'DECIMALS', 'Prices',
                                    'North American Industry Classification System (NAICS)'],
                                   axis=1)

        self.data = self.data.rename(columns={'REF_DATE': 'Date', 'VALUE': 'GdpRetailValue'})

        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

        self.display_data()

        return self.data

    def process_retail_data(self) -> pd.DataFrame:
        """
        Process the retail dataframe
        """
        init(autoreset=True)

        self.data = self.data[(self.data['GEO'] == "Ontario")
                              & (self.data['North American Industry Classification '
                                           'System (NAICS)'] == "Retail trade ["
                                                                "44-45]")
                              & (self.data['Adjustments'] == "Seasonally adjusted")]

        self.data = self.data.drop(['GEO', 'DGUID', 'Adjustments', 'UOM', 'UOM_ID', 'SCALAR_FACTOR',
                                    'SCALAR_ID', 'VECTOR', 'COORDINATE', 'STATUS', 'SYMBOL',
                                    'TERMINATED', 'DECIMALS',
                                    'North American Industry Classification System (NAICS)'],
                                   axis=1)

        self.data = self.data.rename(columns={'REF_DATE': 'Date', 'VALUE': 'RetailValue'})

        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

        self.display_data()

        return self.data

    def process_covid_data(self) -> pd.DataFrame:
        """
        Process the covid data
        """
        init(autoreset=True)
        case_data = pd.DataFrame.from_dict(self.data['cases'][0])
        case_data['date_report'] = pd.to_datetime(case_data['date_report'], errors='coerce')

        case_data = case_data.rename(columns={'date_report': 'Date'})

        case_series = case_data.resample('MS', on='Date',
                                         convention='end')['cases'].sum()
        case_series.name = 'Cases'

        active_data = pd.DataFrame.from_dict(self.data['active'][0])
        active_data['date_active'] = pd.to_datetime(active_data['date_active'], errors='coerce')

        active_data = active_data.rename(columns={'date_active': 'Date'})

        active_series = active_data.resample('MS', on='Date',
                                             convention='end')['active_cases'].sum()
        active_series.name = 'Active'

        # self.data = pd.concat([case_series, active_series], axis=1)
        self.data = pd.DataFrame(dict(cases=case_series, active=active_series)).reset_index()

        self.display_data()

        return self.data

    def display_data(self) -> None:
        """
        Displays the processed dataset header
        """
        print("[INFO]: Pandas dataframe contains " + str(self.data.size) + " data points"
              + " shaped " + str(self.data.shape))
        print(Fore.BLUE + "[DATA]: PROCESSED")
        print(self.data.head(5))

        deinit()


def done_processing(valid: bool) -> None:
    """
    After all files have been processed
    """
    if valid:
        print(Fore.GREEN + "[SUCCESS]: Done processing all data successfully.")
    else:
        print(Fore.RED + "[ERROR]: There was an error processing files. Please try again.")


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['gc', 'pandas', 'colorama'],
        'allowed-io': ['__init__', 'display_data', 'clear_data', 'done_processing']
    })
