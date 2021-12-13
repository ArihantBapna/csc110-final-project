"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Child to Requester that maps to making WDS requests to and from StatisticsCanada
Following https://www.statcan.gc.ca/en/developers/wds/user-guide#a10-2 guidelines to make calls
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet

import json
import os
import zipfile
from dataclasses import dataclass
from pathlib import Path
from colorama import deinit, Fore, init
from requests import Response
from tqdm import tqdm
from reqester import Requester


@dataclass
class StatCan(Requester):
    """
    Requesting a cube from Statistics Canada
    """
    pid: int

    def __init__(self, pid: int, needed: bool) -> None:
        self.pid = pid
        endpoint = "https://www150.statcan.gc.ca/t1/wds/rest/"
        super().__init__(endpoint, needed)
        self.headers = {"content-type": "application/json"}

    def get_cube_metadata(self) -> str:
        """
        Returns the Cube MetaData for the initialized Cube
        """
        self.endpoint = "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"
        self.body = json.dumps([{"productId": self.pid}])
        response = self.post_request(self.body)
        self.assert_request_statcan(response)
        return response

    def get_cube_metadata_backup(self, link: str, local_dir: str) -> str:
        """
        Returns the Cube MetaData for the initialized Cube from the backup datasource
        :return:
        """
        self.endpoint = link
        response = self.get_stream()
        self.assert_request()

        self.response = response

        if response != Response():

            header = self.get_header()
            content_length = int(header.get('content-length', 0))

            filename = "cube_metadata.json"
            file_link = download_files(local_dir, filename, content_length, response)
            return file_link
        else:
            return "Failed"

    def get_full_table_csv_link(self) -> str:
        """
        Returns the link to the full csv zip file for a pid
        """
        self.endpoint = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/" + str(
            self.pid) + "/en"
        response = self.get_request()

        if response == '' or response is None:
            self.fail = True
        return response

    def get_table_downloaded(self, link: str, local_dir: str) -> None:
        """
        Download the csv zip from the link and return the path to the zip file
        """
        self.endpoint = link

        response = self.get_stream()
        self.response = response

        header = self.get_header()
        content_length = int(header.get('content-length', 0))

        filename = self.endpoint.split("/")[-1]

        file_link = download_files(local_dir, filename, content_length, response)

        print("[INFO]: Extracting " + filename)
        with zipfile.ZipFile(file_link, "r") as zipy:
            zip_filename = filename.replace("-eng", "").replace("zip", "csv")
            zipy_info = zipy.infolist()

            # Find the data file and extract it from the zip file saving it as data.csv
            for zip_file in zipy_info:
                if zip_file.filename == zip_filename:
                    zip_file.filename = "data.csv"
                    zipy.extract(zip_file, path=local_dir)
        zipy.close()

        delete_temp_files(file_link, filename, local_dir)

        deinit()

    def get_table_downloaded_backup(self, link: str, local_dir: str, filename: str) -> None:
        """
        Download the csv zip file from the backup data source
        :param link:
        :param local_dir:
        :param filename:
        :return:
        """

        self.endpoint = link
        response = self.get_stream()
        self.response = response

        header = self.get_header()
        content_length = int(header.get('content-length', 0))

        file_link = download_files(local_dir, filename, content_length, response)
        print("[INFO]: Extracting " + filename)

        with zipfile.ZipFile(file_link, "r") as zipy:
            # Find the data file and extract it from the zip file saving it as data.csv
            zipy_info = zipy.infolist()
            for zip_file in zipy_info:
                if zip_file.filename == "data.csv":
                    zipy.extract(zip_file, path=local_dir)
        zipy.close()

        delete_temp_files(file_link, filename, local_dir)

        deinit()

    def assert_request_statcan(self, response: str) -> None:
        """
        Confirm that the WDS request resulted in a successful payload transfer
        """
        init(autoreset=True)

        if response == "Failed" or response == "" or response is None:
            self.fail = True
            return

        data = json.loads(json.dumps(response))
        if not len(data) > 0:
            if self.needed:
                print(Fore.RED
                      + "[FATAL ERROR]: Response "
                      + str(data)
                      + " is not a valid WDS response")
            else:
                print(Fore.YELLOW + "[WARNING]: Response "
                      + str(data)
                      + " is not a valid WDS response. Continuing based on last fetch")
                self.fail = True
        status = data[0]['status']

        if status != "SUCCESS":
            if self.needed:
                print(Fore.RED
                      + "[FATAL ERROR]: WDS Request to "
                      + self.endpoint
                      + " failed with status " + status)
                self.fail = True
            else:
                print(Fore.YELLOW
                      + "[WARNING]: WDS Request to"
                      + self.endpoint
                      + " failed with stats" + status + ". Continuing based on last fetch")
        deinit()


def download_files(local_dir: str, filename: str, content_length: int,
                   response: Response) -> str:
    """
    Download a given file from a stream with a progress bar displayed
    :param local_dir:
    :param filename:
    :param content_length:
    :param response:
    """
    block_size = 1024  # 1 Kilobyte
    file_link = local_dir + "/" + filename

    print("[INFO]: Downloading " + filename + " to " + local_dir)

    # Create a progress bar
    progress_bar = tqdm(total=content_length, unit="iB", unit_scale=True)

    # Create the temp zip file as a stream
    with open(file_link, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    file.close()
    progress_bar.close()

    print(Fore.GREEN + "[SUCCESS]: Finished downloading "
          + file_link)

    return file_link


def delete_temp_files(file_link: str, filename: str, local_dir: str) -> None:
    """
    Deletes the temporary zip files
    :param local_dir:
    :param file_link:
    :param filename:
    """
    # Delete the temp zip file
    if os.path.exists(file_link):
        os.remove(file_link)
    else:
        print(Fore.YELLOW + "[WARNING]: Could not delete " + filename + ". File doesn't exist")

    print(Fore.GREEN
          + "[SUCCESS]: Finished extracting " + filename + " to "
          + str(Path(local_dir + "/data.csv").absolute()))


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["pathlib", "colorama", "cube", "openvcovid", "os", "json", "pandas",
                          "requests", "tqdm", "reqester", "zipfile"],
        'allowed-io': ['__init__', 'get_cube_metadata', 'get_cube_metadata_backup',
                       'get_full_table_csv_link', 'download_files', 'get_table_downloaded',
                       'get_table_downloaded_backup', 'delete_temp_files', 'assert_request_statcan']
    })
