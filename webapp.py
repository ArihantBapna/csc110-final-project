"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Class that initializes the webapp for our project
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
from dataclasses import dataclass

import dash
from colorama import Fore
from dash import dcc
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from graphing import Graphing


@dataclass
class WebApp:
    """
    Class representing the WebApp that displays our app data
    """
    app: dash.Dash
    graphs: Graphing

    def __init__(self, graphs) -> None:
        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.graphs = graphs

    def set_layout(self) -> None:
        """
        Creates the layout for the app
        """
        print("[INFO]: Setting the layout for the app")
        # Navbar
        inline_text = dbc.Row(
            [
                dbc.Col(html.P(children="A Webapp for our Analysis running on Python using "
                                        "Waitress, Dash and Plot.ly",
                               className="m-0 text-white"))
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        )

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(dbc.NavbarBrand("CSC110 Final Project", className="ms-2")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://github.com/ArihantBapna/csc110-project",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        inline_text,
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ]
            ),
            color="dark",
            dark=True,
        )

        @self.app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n: object, is_open: object) -> object:
            """
            Toggle the navbar collapse
            :param n:
            :param is_open:
            :return:
            """
            if n:
                return not is_open
            return is_open

        self.app.title = "CSC110 Final Project"
        self.app.layout = html.Div([
            navbar,
            dcc.Graph(
                id="covid-unemployment",
                figure=self.graphs.graph_covid_on_unemployment()
            ),
            dcc.Graph(
                id="covid-ontario",
                figure=self.graphs.graph_covid_cases_on_time()
            ),
            dcc.Graph(
                id="employment-graph",
                figure=self.graphs.graph_employment_on_time()
            ),
            dcc.Graph(
                id="gdp-graph",
                figure=self.graphs.graph_gdp_on_time()
            ),
            dcc.Graph(
                id="gdp-all-graph",
                figure=self.graphs.graph_gdp_all_time()
            ),
            dcc.Graph(
                id="retail-graph",
                figure=self.graphs.graph_retail_on_time()
            ),
            dcc.Graph(
                id="cpi-graph",
                figure=self.graphs.graph_cpi_on_time()
            ),
            dcc.Graph(
                id="cpi-all-graph",
                figure=self.graphs.graph_cpi_on_all_time()
            ),
        ])
        print(Fore.GREEN + "[SUCCESS] Set Web App layout")

    def get_app(self) -> object:
        """
        Returns the app for the project
        """
        return self.app
