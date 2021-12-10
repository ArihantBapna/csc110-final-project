"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Parent class to initiate REST/Stream api calls over http/s and collect data
"""
import time
from dataclasses import dataclass

import requests
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
        response = requests.get(url=self.endpoint, params=self.body, headers=self.headers)
        self.response = response

        if not self.assert_request():
            self.get_request()
        else:
            if not self.fail:
                return response.json()
            else:
                return ''

    def post_request(self, data: str) -> str:
        """
        Returns a post request's response
        """
        response = requests.post(url=self.endpoint, data=data, params=self.body, headers=self.headers)
        self.response = response

        if not self.assert_request():
            self.post_request(data)
        else:
            if not self.fail:
                return response.json()
            else:
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

    def get_stream(self) -> Response:
        """
        Return a stream response
        """
        # Streaming, so we can iterate over the response.
        response = requests.get(self.endpoint, stream=True)

        # Ensure the stream is alive
        if not self.assert_request():
            self.get_stream()
        else:
            if not self.fail:
                return response
            else:
                return Response()

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

            self.attempts += 1
            if self.attempts > 5:
                if self.needed:
                    print(Fore.RED
                          + "[FATAL ERROR]: Could not complete request to "
                          + self.endpoint)
                    exit(1)
                else:
                    print(Fore.YELLOW
                          + "[WARNING]: Could not complete request to "
                          + self.endpoint
                          + "Continuing based on last fetched.")
                    self.fail = True
                    return True

            print("[INFO]: Retrying in 5 seconds"
                  + "(" + str(self.attempts) + "/5)")
            time.sleep(5)
            deinit()

            return False
        else:
            deinit()
            self.attempts = 0
            return True
