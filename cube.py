"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Child to Requester that sends requests to the GDP of StatCan
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from colorama import deinit, Fore, init
from statcan import StatCan


@dataclass
class Cube(StatCan):
    """
    Abstract class mirroring a cube from WDS StatisticsCanada
    """
    metadata: dict
    local_dir: str
    update_dataset: bool
    backup: str
    try_backup: bool

    def __init__(self, pid: int, local_dir: str) -> None:
        init(autoreset=True)

        # Assume that we don't need to try the backup server
        self.try_backup = False

        # Set the backup links in-case it's needed
        self.backup = "https://backup-server-csc110.herokuapp.com/"

        # Assume the dataset doesn't need to be updated
        self.update_dataset = False

        self.local_dir = local_dir

        # Initialize local directory hierarchy
        needed = self.initialize_local_dir()

        # Initialize metadata file
        metadata_file = Path(self.local_dir + "/cube_metadata.json")
        needed = self.run_metadata_tests(metadata_file, needed)

        # Initialize the StatCan Requester
        super().__init__(pid, needed)

        # Attempt to grab the metadata from StatCan for the given cube
        response = self.get_cube_metadata()

        # Check if the request/response had a failure
        if self.fail:
            self.response_sanitation_check()
            # On Failing the sanitation check try the backup server
            if needed:
                link = self.backup + "metadata?filename=" + str(self.pid) + ".json"
                # Attempt to grab the metadata from the backup s
                response = self.get_cube_metadata_backup(link, local_dir)

                if response == "Failed":
                    print(
                        Fore.RED + "[FATAL ERROR]: Could not connect to the backup server either. "
                                   "Servers may be down or you may not "
                                   "be connect to the internet.")
                    exit(1)
                else:
                    print(Fore.GREEN + "[SUCCESS]: Downloaded metadata file from the backup server")

            else:
                print(Fore.YELLOW + "[WARNING]: Could not establish connection "
                                    "to test for new data. Assuming current meta data is latest.")

            # First check if the data.csv file exists
            data_file = Path(self.local_dir + "/data.csv")
            data_needed = not data_file.is_file()

            # Do the initialization for the dataset
            print("[INFO]: Trying to find the data file for " + self.local_dir)

            if data_needed:
                print(Fore.YELLOW
                      + "[WARNING]: Could not find the data file for "
                      + self.local_dir
                      + ". Attempting to build a new one")

                csv_link_response = self.get_full_table_csv_link()
                if not self.fail:
                    csv_link_response = json.loads(json.dumps(csv_link_response))
                    self.save_data_file(csv_link_response)
                else:
                    print(Fore.RED
                          + "[FATAL ERROR]: Could not make a request to " + self.endpoint
                          + ". Service may be down. Trying to use backup")

                    link = self.backup + "data?filename=" + str(self.pid) + ".zip"
                    self.get_table_downloaded_backup(link, local_dir, (str(self.pid) + ".zip"))

            else:
                print(Fore.GREEN
                      + "[SUCCESS] Found data.csv in the cube folder " + local_dir
                      + ". Assuming the dataset is correct")

        # If no failure in request/response
        else:
            # Save the metadata to the respective file
            self.save_metadata_file(response, metadata_file)
            # Now we initialize the dataset
            csv_link_response = self.get_full_table_csv_link()

            # Again check if the request/response had a failure
            if self.fail:
                self.response_sanitation_check()

            else:
                # Save the main dataset for the cube
                self.save_data_file(csv_link_response=csv_link_response)

        deinit()

    def initialize_local_dir(self) -> bool:
        """
        Tries to initialize the local directory for the cube
        """
        # Check if the cube local_dir exists
        if Path(self.local_dir).is_dir():
            print("[INFO]: Found cube in "
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
                os.mkdir(Path(self.local_dir))
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

    def run_metadata_tests(self, metadata_file: Path, needed: bool) -> bool:
        """
        Creates the initial metadata_file and tests it if it already exists.
        Returns whether the statcan requests are to be needed
        """
        # Check if the metadata file for the cube exists
        if not metadata_file.is_file():
            print(Fore.YELLOW
                  + "[WARNING]: Could not find "
                  + str(metadata_file.absolute()))
            needed = True
        # If it does exist, attempt to read it and assign it to the cube
        else:
            try:
                with open(metadata_file) as file:
                    try:
                        self.metadata = json.load(file)
                    except json.decoder.JSONDecodeError:
                        print(Fore.RED
                              + "[ERROR]: Corrupted metadata file for "
                              + str(metadata_file.absolute()))
                        needed = True
                    else:
                        print(Fore.GREEN + "[SUCCESS]: Decoded metadata for "
                              + str(metadata_file.absolute()))
            except IOError as error:
                print(Fore.RED
                      + "[FATAL ERROR]: Could not read saved metadata file for "
                      + str(metadata_file.absolute())
                      + str(error)
                      + " -- Delete it and try again.")
                exit(1)  # exit marked here if the metadata file is corrupted
            else:
                if not needed:
                    print(Fore.GREEN + "[SUCCESS]: Finished reading "
                          + str(metadata_file.absolute())
                          + ". Data from "
                          + self.metadata['object']['releaseTime'])
        return needed

    def response_sanitation_check(self) -> None:
        """
        Alerts to initialization progress on fail
        """
        if self.needed:
            print(Fore.RED
                  + "[FATAL ERROR]: Request to initialize metadata for "
                  + self.local_dir
                  + " failed from " + self.endpoint + ". Attempting to use the backup server")
            # exit(1)
        else:
            print(Fore.YELLOW
                  + "[WARNING]: Request to initialize file"
                  + self.local_dir
                  + " failed. No updates will be made.")

    def save_metadata_file(self, response: str, metadata_file: Path) -> None:
        """
        Attempt to save the metadata file if new data available
        :param response:
        :param metadata_file:
        """
        # Consume the payload data
        data = json.loads(json.dumps(response))[0]

        # If the file is needed, then try and save it
        if self.needed:
            try:
                with open(metadata_file, "w") as file:
                    json.dump(data, file, indent=4, sort_keys=False)
            except IOError as error:
                print(Fore.RED
                      + "[FATAL ERROR]: Unable to save the metadata to "
                      + self.local_dir
                      + str(error) + ". Ensure adequate permissions.")
                exit(1)
            else:
                print(
                    "[INFO]: Saved metadata to " + str(metadata_file.absolute()) + " successfully.")

        # If the file is not immediately needed, compare cubeEndDate

        else:
            curr_response_time = datetime.strptime(self.metadata['object']['cubeEndDate'],
                                                   '%Y-%m-%d').date()
            new_response_time = datetime.strptime(data['object']['cubeEndDate'], '%Y-%m-%d').date()

            # If the data just received is newer than the data stored save the new data
            if new_response_time > curr_response_time:
                self.update_dataset = True
                try:
                    with open(metadata_file, "w") as file:
                        json.dump(data, file)
                except IOError as error:
                    print(Fore.YELLOW
                          + "[Warning]: Unable to save the new metadata to "
                          + self.local_dir
                          + str(error)
                          + ". Ensure adequate permissions. Continuing based on last fetched.")
                else:
                    print(Fore.GREEN + "[SUCCESS]: updated "
                          + str(metadata_file.absolute())
                          + " with data from " + data['object']['releaseTime'])

    def save_data_file(self, csv_link_response: str) -> None:
        """
        Attempt to save the data.csv file for the cube
        :param csv_link_response:
        """
        # Consume the json response
        csv_link_response = json.loads(json.dumps(csv_link_response))
        print("[INFO]: Trying to find the data file for " + self.local_dir)
        # First check if the data.csv file exists
        data_file = Path(self.local_dir + "/data.csv")

        if not data_file.is_file():
            print(Fore.YELLOW
                  + "[WARNING]: Could not find the data file for "
                  + self.local_dir
                  + ". Attempting to build a new one")
            self.update_dataset = True

        if self.update_dataset:
            self.get_table_downloaded(link=csv_link_response['object'], local_dir=self.local_dir)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["pathlib", "colorama", "cube", "openvcovid", "os", "json", "datetime",
                          "statcan"],
        'allowed-io': ['__init__', 'initialize_local_dir', 'save_data_file', 'save_metadata_file',
                       'response_sanitation_check', 'run_metadata_tests']
    })
