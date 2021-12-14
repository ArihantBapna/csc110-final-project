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
from colorama import Fore


class Graphing:
    """
    Initialize the plot graphing tools
    """

    employment: pd.DataFrame
    cpi: pd.DataFrame
    gdp: pd.DataFrame
    retail: pd.DataFrame
    covid: pd.DataFrame

    def __init__(self, all_data: tuple) -> None:
        print("[INFO]: Initializing the graphing engine")
        self.employment = all_data[0]
        self.cpi = all_data[1]
        self.gdp = all_data[2]
        self.retail = all_data[3]
        self.covid = all_data[4]

    def graph_employment_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph unemployment as a time series
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Unemployment AFTER Covid")
        df = self.employment
        df = df[(df['Date'].dt.year == 2020) | (df['Date'].dt.year == 2021)]

        fig = px.line(df, x='Date', y='UnemploymentValue', facet_col='Sex', color="Age",
                      markers=True,
                      labels={
                          "Date": "Date",
                          "UnemploymentValue": "Unemployment (%) ",
                          "Age": "Age Range"
                      },
                      title="Unemployment over time during Covid")
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        })
        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_cpi_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph the consumer price index as a time series
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for CPI AFTER Covid")
        df = self.cpi
        df = df[(df['Date'].dt.year == 2020) | (df['Date'].dt.year == 2021)]

        fig = px.scatter(df, x='Date', y='CpiValue', trendline="ols",
                         labels={
                             'Date': 'Date',
                             'CpiValue': 'Consumer Price Index'
                         },
                         title="Consumer price index over time during Covid")

        # fig.update_layout({
        #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        #     'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        # })

        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_cpi_on_all_time(self) -> plotly.graph_objs.Figure:
        """
        Graph cpi over all time
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for CPI BEFORE Covid")
        df = self.cpi
        df = df[(df['Date'].dt.year < 2020)]

        fig = px.scatter(df, x='Date', y='CpiValue', trendline="ols",
                         labels={
                             'Date': 'Date',
                             'CpiValue': 'Consumer Price Index'
                         },
                         title="Consumer price index over time pre Covid")
        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_gdp_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph Retail GDP Contributions During Covid
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Retail GDP Contributions During Covid")
        df = self.gdp
        df = df[(df['Date'].dt.year == 2020) | (df['Date'].dt.year == 2021)]

        fig = px.line(df, x='Date', y='GdpRetailValue', markers=True,
                      labels={
                          'Date': 'Date',
                          'GdpRetailValue': 'Retail GDP'
                      },
                      title="Retail GDP over time during Covid")
        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_gdp_all_time(self) -> plotly.graph_objs.Figure:
        """
        Graph GDP over all Time
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Retail GDP Contributions over all time")
        df = self.gdp

        fig = px.line(df, x='Date', y='GdpRetailValue', markers=False,
                      labels={
                          'Date': 'Date',
                          'GdpRetailValue': 'Retail GDP'
                      },
                      title="Retail GDP All Time")
        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_retail_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph Retail during Covid
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Retail GDP Contributions During Covid")
        df = self.retail
        df = df[(df['Date'].dt.year == 2020) | (df['Date'].dt.year == 2021)]

        fig = px.line(df, x='Date', y='RetailValue', markers=True,
                      labels={
                          'Date': 'Date',
                          'RetailValue': 'Retail Value'
                      },
                      title="Retail over time during Covid")
        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_covid_cases_on_time(self) -> plotly.graph_objs.Figure:
        """
        Graph Covid Cases During Covid
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Covid Cases During Covid")
        df = self.covid

        fig = px.bar(df, x='Date', y='cases', color='active',
                     labels={
                         'Date': 'Date',
                         'cases': 'New Cases',
                         'active': 'Active Cases'
                     },
                     title="Covid cases over time")

        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")
        return fig

    def graph_covid_on_unemployment(self) -> plotly.graph_objs.Figure:
        """
        Graph covid cases vs retail
        """
        print(Fore.MAGENTA + "[GRAPH]: Generating graph for Covid Cases vs Unemployment")
        df = pd.merge(self.covid, self.employment, on='Date')

        fig = px.scatter(df, x='cases', y='UnemploymentValue', facet_col='Age', facet_row='Sex',
                         color='active',
                         trendline='ols',
                         labels={
                             'UnemploymentValue': 'Unemployment (%) ',
                             'cases': 'New Cases'
                         },
                         title="Covid Cases vs Unemployment")

        # fig.show()
        print(Fore.BLUE + "[DATA]: GRAPHING: ")
        print(df.head(10))
        print(Fore.GREEN + "[SUCCESS]: Generated graph from above data")

        return fig
