"""
CSC110 Project for Arihant Bapna, Hongzip Kim, and Nicholas Macasaet.

Plotly Graphing class for the final projects
"""
# Copyright (c) 2021. Arihant Bapna  - All Rights Reserved| You may use this code under the terms
# of the MIT License for the simple fact that I was too lazy to write my own license You should
# have received a copy of the license with this project, if not and for any other queries contact
# me at: a.bapna@mail.utoronto.ca This code is part of the CSC110F 2021 Final Project for the
# group consisting of Arihant Bapna, Hongzip Kim and Nick Macasaet
import pandas as pd
import plotly.express as px
import plotly.graph_objs


class Graphing:
    """
    Initialize the plot graphing tools
    """

    employment: pd.DataFrame
    cpi: pd.DataFrame
    gdp: pd.DataFrame
    retail: pd.DataFrame
    covid: pd.DataFrame

    def __init__(self) -> None:
        print("[INFO]: Initializing the graphing engine")

    def set_employment(self, employment: pd.DataFrame):
        """
        Sets the employment data
        """
        print(employment)
        self.employment = employment
        self.graph_employment_on_time()

    def graph_employment_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph unemployment as a time series
        """
        df = self.employment[self.employment['Age'] == '25 to 54 years']
        fig = px.histogram(df, x='Date')
        fig.update_layout(bargap=0.2)
        fig.show()

        return fig
