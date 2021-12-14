"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Class that starts the server for our project

Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
of the MIT License. You should have received a copy of the license with this project,
if not and for any other queries contact me at: a.bapna@mail.utoronto.ca This code is part of the
CSC110F 2021 Final Project for the group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
"""

import webbrowser
import dash
from colorama import Fore
from waitress import serve


class PlotServer:
    """
    Runs the server for the plotly app
    """
    app: dash.Dash

    def __init__(self, app) -> None:
        self.app = app

    def run_server(self) -> None:
        """
        Runs the dash server for the app
        """
        print("[INFO]: Trying to run the server on http://localhost:8050")
        webbrowser.open("http://localhost:8050")
        print(Fore.GREEN + "[SUCCESS]: Server started on http://localhost:8050")
        serve(self.app.server, host="0.0.0.0", port="8050")


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ["webbrowser", "dash", "colorama", "waitress"],
        'allowed-io': ['run_server']
    })
