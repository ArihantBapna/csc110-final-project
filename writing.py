"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Class that writes out the processed data
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from colorama import Fore


@dataclass
class Writing:
    """
    Write out processed data
    """
    data_found: bool
    local_dir: str

    def __init__(self, working_dir: str) -> None:
        # Check if the processed_data folder is initialized
        local_dir = "/processed_data"
        if Path(working_dir + local_dir).is_dir():
            print(Fore.GREEN + "[SUCCESS] Found output directory already at " + str(
                Path(working_dir + local_dir).absolute()))
            self.data_found = True
        else:
            try:
                os.mkdir(Path(working_dir + local_dir))
            except OSError as error:
                print(Fore.RED + "[FATAL ERROR]: Unable to create "
                      + local_dir
                      + str(error)
                      + ". Ensure adequate permissions.")
                exit(1)  # exit marked here if unable to create/find the cube directory
            else:
                print(Fore.GREEN + "[SUCCESS]: Created "
                      + str(Path(working_dir + local_dir).absolute()))
                self.local_dir = working_dir + local_dir
            self.data_found = False

    def save_csv_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save the processed data
        """
        try:
            df.to_csv(self.local_dir + "/" + filename)
        except OSError as error:
            print(Fore.RED + "[FATAL ERROR]: Unable to create " + filename + "\n" + str(error))
        else:
            print(Fore.GREEN + "[SUCCESS]: Created "
                  + str(Path(self.local_dir + "/" + filename).absolute()))
