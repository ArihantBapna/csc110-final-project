"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

The main file to run our amazing project
"""
# Copyright (c) 2021. Arihant Bapna, Hongzip Kim and Nick Macasaet  - All Rights Reserved|
# You may use this code under the terms of the MIT License for the simple fact that I was too lazy
# to write my own license. You should have received a copy of the license with this project,
# if not and for any other queries contact me at: a.bapna@mail.utoronto.ca
# This code is part of the CSC110F 2021 Final Project for the group consisting of Arihant Bapna,
# Hongzip Kim and Nick Macasaet

import os
import sys
from pathlib import Path
from colorama import Fore

from graphing import Graphing
from server import PlotServer
from webapp import WebApp
from writing import Writing


def main() -> int:
    """The main entry into the app"""
    from aggregate import Aggregate
    from reading import Reading

    working_dir = "data"
    initialize_working_dir(working_dir)

    write = Writing(working_dir)
    reader = Reading(working_dir, write)
    if not write.data_found:
        agg = Aggregate(working_dir)
        agg.initialize_all_files()

        print("Finished data downloading")
        reader.do_all_read()
    else:
        print("[INFO]: Found processed data in folder. Assuming it is right")
    all_data = reader.do_all_processed_read()
    graphing = Graphing(all_data)

    # graphing.graph_employment_on_time()
    # graphing.graph_cpi_on_time()
    # graphing.graph_cpi_on_all_time()
    # graphing.graph_gdp_on_time()
    # graphing.graph_gdp_all_time()
    # graphing.graph_retail_on_time()
    # graphing.graph_covid_cases_on_time()
    # graphing.graph_covid_on_unemployment()

    webapp = WebApp(graphs=graphing)
    webapp.set_layout()
    server = PlotServer(webapp.get_app())
    server.run_server()

    return 0


def initialize_working_dir(working_dir: str) -> None:
    """
    Initialize the working directory
    :param working_dir:
    :return:
    """
    path = Path(working_dir)
    if not path.is_dir():
        try:
            os.mkdir(path)
        except OSError as error:
            print(Fore.RED + "[FATAL ERROR]: Unable to create "
                  + str(path.absolute())
                  + str(error)
                  + ". Ensure adequate permissions.")
            exit(1)  # exit marked here if unable to create/find the cube directory
        else:
            print(Fore.GREEN + "[SUCCESS]: Created "
                  + str(path.absolute()))


if __name__ == '__main__':
    os.system("pip3 install -r requirements.txt")
    sys.exit(main())
