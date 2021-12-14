"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Attempts to create covid data tables from main source or backup source

Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
of the MIT License. You should have received a copy of the license with this project,
if not and for any other queries contact me at: a.bapna@mail.utoronto.ca This code is part of the
CSC110F 2021 Final Project for the group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
"""

import json
import os
import pathlib
from dataclasses import dataclass
import pandas
from colorama import Fore, init
from requests import Response
from tqdm import tqdm

from requester import Requester


@dataclass
class OpenCovid(Requester):
    """
    Abstract class mirroring the json response from OpenCovid
    """
    prov: str
    local_dir: str

    def __init__(self, prov: str, local_dir: str) -> None:
        init(autoreset=True)

        self.prov = prov
        endpoint = "https://api.opencovid.ca/timeseries?&loc=" + self.prov

        self.local_dir = local_dir
        self.initialize_local_dir()

        print("[INFO]: Attempting to aggregate Covid Data for province " + self.prov)

        file = self.prov + ".json"
        covid_path = pathlib.Path(local_dir + "/" + file)

        if covid_path.is_file():
            print(Fore.GREEN + "[SUCCESS]: Found covid data at " + str(covid_path.absolute()))
            needed = False
        else:
            print(Fore.YELLOW
                  + "[WARNING]: Could not find covid data at " + str(covid_path.absolute()))
            needed = True

        super().__init__(endpoint, needed)

        if self.needed:
            # Assuming you need the file downloaded
            self.response = self.get_covid_data()

        else:
            # If you don't need to update the data just return
            return

        result = "Failed"
        if self.fail:
            print(Fore.RED + "[FATAL ERROR]: Could not grab covid data from " + self.endpoint
                  + ". Trying to use backup")

            backup = "https://backup-server-csc110.herokuapp.com/"
            self.endpoint = backup + "covid?filename=" + file
            self.response = self.get_covid_data()

            if self.fail:
                print(Fore.RED
                      + "[FATAL ERROR]: Could not connect to backup database at" + self.endpoint
                      + ". Please check your internet connection and try again")
                exit(1)
            else:
                result = self.save_covid_data_from_stream()
        else:
            result = self.save_covid_data_from_stream()

        if result == "Failed":
            print(Fore.RED + "[FATAL ERROR]: Could not save covid data through any server."
                  + "Please try again later")
            exit(1)
        else:
            print(Fore.GREEN + "[SUCCESS]: Initialized Covid data for " + self.prov)
            # self.convert_json_to_csv(filename=file)

    def convert_json_to_csv(self, filename: str) -> None:
        """
        Attempts to convert the json covid data to csv covid data
        :return:
        """
        self.fail = False
        file_link = self.local_dir + "/" + filename
        export_link = self.local_dir + "/" + self.prov + ".csv"
        print("[INFO]: Attempting to convert " + str(pathlib.Path(file_link))
              + " to a csv file")

        with open(file_link) as f:
            data = json.load(f)

        json_covid_data = pandas.json_normalize(data)

        json_covid_data.to_csv(export_link, index=False)

        print(Fore.GREEN + "[SUCCESS]: Converted the file to a csv")

    def get_covid_data(self) -> Response:
        """
        Attempts to grab covid data from the main data source
        """
        self.fail = False
        print("[INFO]: Attempting to download covid data for "
              + self.prov + " from "
              + self.endpoint)
        response = self.get_stream()

        if response == Response() or response is None:
            self.fail = True

        return response

    def save_covid_data_from_stream(self) -> str:
        """
        Saves the streamed covid data to a json file
        :return:
        """

        if self.response != Response() or self.response is not None:
            header = self.get_header()
            content_length = int(header.get('content-length', 0))

            filename = self.prov + ".json"
            file_link = self.download_covid_data_from_stream(filename, content_length)
            return file_link
        else:
            return "Failed"

    def download_covid_data_from_stream(self, filename: str, content_length: int) -> str:
        """
         Download the given file from a stream with a progress bar displayed
        """
        block_size = 1024  # 1 Kilobyte
        file_link = self.local_dir + "/" + filename

        print("[INFO]: Downloading " + filename + " to " + self.local_dir)

        # Create a progress bar
        progress_bar = tqdm(total=content_length, unit="iB", unit_scale=True)

        # Create the temp zip file as a stream
        with open(file_link, "wb") as file:
            for data in self.response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        file.close()
        progress_bar.close()

        print(Fore.GREEN + "[SUCCESS]: Finished downloading "
              + file_link)

        return file_link

    def initialize_local_dir(self) -> bool:
        """
        Tries to initialize the local directory for the cube
        """
        # Check if the cube local_dir exists
        if pathlib.Path(self.local_dir).is_dir():
            print("[INFO]: Found covid stream in "
                  + self.local_dir
                  + ". Attempting to read.")
            needed = False
        else:
            print(Fore.YELLOW
                  + "[WARNING]: Could not find cube "
                  + self.local_dir
                  + ". Attempting to create one.")
            needed = True
            try:
                os.mkdir(pathlib.Path(self.local_dir))
            except OSError as error:
                print(Fore.RED + "[FATAL ERROR]: Unable to create "
                      + self.local_dir
                      + str(error)
                      + ". Ensure adequate permissions.")
                exit(1)  # exit marked here if unable to create/find the cube directory
            else:
                print(Fore.GREEN + "[SUCCESS]: Created "
                      + self.local_dir)
        return needed


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["pathlib", "colorama", "cube", "openvcovid", "os", "json", "pandas",
                          "requests", "tqdm", "reqester"],
        'allowed-io': ['__init__', 'convert_json_to_csv', 'get_covid_data',
                       'save_covid_data_from_stream', 'download_covid_data_from_stream',
                       'initialize_local_dir']
    })
