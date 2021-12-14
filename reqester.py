"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Parent class to initiate REST/Stream api calls over http/s and collect data

Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
of the MIT License. You should have received a copy of the license with this project,
if not and for any other queries contact me at: a.bapna@mail.utoronto.ca This code is part of the
CSC110F 2021 Final Project for the group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
"""

import time
from dataclasses import dataclass
import requests
import urllib3.exceptions
from colorama import deinit, Fore, init
from requests import Response
from requests.structures import CaseInsensitiveDict


@dataclass
class Requester:
    """
    Using this as a parent to initialize requests to every data site
    """
    endpoint: str
    headers: dict
    body: str
    attempts: int
    needed: bool
    fail: bool
    response: Response

    def __init__(self, endpoint: str, needed: bool) -> None:
        self.endpoint = endpoint
        self.headers = {}
        self.body = ""
        self.attempts = 0
        self.needed = needed
        self.fail = False

    def set_body(self, body: str) -> None:
        """
        Sets the body for the request
        :param body:
        """
        self.body = body

    def set_headers(self, headers: dict) -> None:
        """
        Sets the header for the request
        :param headers:
        """
        self.headers = headers

    def get_request(self) -> str:
        """
        Returns a get request's response
        """
        try:
            response = requests.get(url=self.endpoint, params=self.body, headers=self.headers)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
                urllib3.exceptions.ProtocolError, ConnectionResetError):
            return ''
        else:
            self.response = response
            if not self.assert_request():
                self.get_request()
            else:
                if not self.fail:
                    return response.json()
                else:
                    return ''
        return ''

    def post_request(self, data: str) -> str:
        """
        Returns a post request's response
        """
        try:
            response = requests.post(url=self.endpoint, data=data, params=self.body,
                                     headers=self.headers)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
                urllib3.exceptions.ProtocolError, ConnectionResetError):
            return ''
        else:
            self.response = response
            if not self.assert_request():
                self.post_request(data)
            else:
                if not self.fail:
                    return response.json()
                else:
                    return ''
        return ''

    def get_header(self) -> CaseInsensitiveDict:
        """
        Returns the header for a request
        """
        head = requests.head(url=self.endpoint, allow_redirects=True)
        header = head.headers

        if not self.assert_request():
            self.get_header()
        else:
            if not self.fail:
                return header
            else:
                return CaseInsensitiveDict()
        return CaseInsensitiveDict()

    def get_stream(self) -> Response:
        """
        Return a stream response
        """
        # Streaming, so we can iterate over the response.
        try:
            response = requests.get(self.endpoint, stream=True)

        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
                urllib3.exceptions.ProtocolError, ConnectionResetError):
            response = Response()
        else:
            print(Fore.GREEN + "[SUCCESS]: Stream initialized to " + self.endpoint)
        self.response = response
        # Ensure the stream is alive
        if not self.assert_request():
            self.get_stream()
        else:
            if not self.fail:
                self.response = response
                return response
            else:
                return Response()
        return Response()

    def catch_response_exception(self, error: any) -> str:
        """
        Handles any exception to connections
        :param error:
        :return:
        """
        if self.needed:
            print(Fore.RED + "[FATAL ERROR]: Connection failed to "
                  + self.endpoint
                  + " "
                  + str(error))
        else:
            print(Fore.YELLOW + "[WARNING]: Connection failed to "
                  + self.endpoint
                  + " "
                  + str(error)
                  + ". Continuing based on last fetch")
        return 'Failed'

    def assert_request(self) -> bool:
        """
        Retry the request if the request fails
        """
        init(autoreset=True)
        self.fail = False
        if self.response.status_code != 200:
            print(Fore.RED
                  + "[ERROR " + str(self.response.status_code) + "]: "
                  + "Could not make the request to "
                  + self.endpoint)

            self.attempts += 3  # Change this back to 1
            if self.attempts > 3:
                if self.needed:
                    print(Fore.RED
                          + "[FATAL ERROR]: Could not complete request to "
                          + self.endpoint)
                else:
                    print(Fore.YELLOW
                          + "[WARNING]: Could not complete request to "
                          + self.endpoint
                          + "Continuing based on last fetched.")
                self.fail = True
                return True

            print("[INFO]: Retrying in 5 seconds "
                  + "(" + str(self.attempts) + "/1)")
            time.sleep(5)
            deinit()

            return False
        else:
            deinit()
            self.attempts = 0
            return True


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["requests", "requests.structures", "colorama",
                          "urllib3.exceptions", "time"],
        'allowed-io': ['set_body', 'get_requests',
                       'post_requests', 'get_header', 'get_stream', 'get_gdrive_stream',
                       'get_confirm_token', 'catch_response_exception', 'assert_request']
    })
