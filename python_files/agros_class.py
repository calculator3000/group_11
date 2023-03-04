""" This module contains one class with the purpose of analyzing agricultural data internationally.
It contains seven methods. Those can download the data, list all the countries of the dataset,
provide a correlation matrix of the outputs, and plot an area chart of the agricultural output
of a choosen country.
It can also compare the output of choosen countries with a line graph, and plot a scatter plot
of fertilizer and output quantity.
Moreover, a choropleth of the total factor productivity for a selected year can be plotted.
"""

import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np


class Agros:
    """
    A class that downloads agricultural data and performs analysis on it.

    Attributes
    ---------------
    data_df: Pandas Dataframe
        dataframe where the downloaded agricultural data can be loaded into

    merge_dict: dict
        a dictionary in order to change the spelling for some countries to allow merging


    Methods
    ---------------
    download_data
        downloads agricultural data from Github, saves it to a download folder
        and creates Pandas DataFrame

    list_countries
        list all the available countries of the dataset

    correlate_quantity
        provides a correlation heatmap of the quality columns

    area_graph
        provides an area graph of the outputs of a selected country or the world

    compare_output
        plots the output columns of selected countries

    gapminder
        provides a scatterplot of fertilizer and output quantity for a selected year

    choropleth
        provided a choropleth plotting the total factor productivity of a selected year

    """

    def __init__(self):
        self.data_df = pd.DataFrame
        self.merge_dict = {
            "United States of America": "United States",
            "Dem. Rep. Congo": "Democratic Republic of Congo",
            "Dominican Rep.": "Dominican Republic",
            "Timor-Leste": "Timor",
            "Eq. Guinea": "Equatorial Guinea",
            "eSwatini": "Eswatini",
            "Solomon Is.": "Solomon Islands",
            "N. Cyprus": "Cyprus",
            "Somaliland": "Somalia",
            "Bosnia and Herz.": "Bosnia and Herzegovina",
            "S. Sudan": "South Sudan",
        }

    def download_data(self):
        """
        Creates a 'downloads' folder, if it doesn't exist.
        Downloads agricultural data from Github repository and saves it to this folder,
        in case it is not already downloaded.
        It also creates Pandas Dataframe from the downloaded csv file.
        """
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        exists = os.path.isfile("downloads/download.csv")

        if not exists:
            response = requests.get(
                "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/"
                "Agricultural%20total%20factor%20productivity%20(USDA)"
                "/Agricultural%20total%20factor%20productivity%20(USDA).csv"
            )
            with open("downloads/download.csv", "wb") as file:
                file.write(response.content)

        self.data_df = pd.read_csv("downloads/download.csv")

        self.geopandas_df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    def list_countries(self):
        """Lists all the countries of the Entity column and removes the duplicates.
        It also cleans the data so that aggregated rows (like Asia) are excluded.

        Returns
        ---------------
        country_list: list
            All countries in the agros_data Entity column

        """
        data_df_new_index = self.data_df.set_index("Entity")
        data_df = data_df_new_index.drop(
            [
                "Asia",
                "Caribbean",
                "Central Africa",
                "Central America",
                "Central Asia",
                "Central Europe",
                "Developed Asia",
                "Developed countries",
                "East Africa",
                "Eastern Europe",
                "Former Soviet Union",
                "High income",
                "Horn of Africa",
                "Latin America and the Caribbean",
                "Least developed countries",
                "Lower-middle income",
                "North Africa",
                "North America",
                "Northeast Asia",
                "Northern Europe",
                "Oceania",
                "Pacific",
                "Sahel",
                "South Asia",
                "Southeast Asia",
                "Southern Africa",
                "Southern Europe",
                "Sub-Saharan Africa",
                "Upper-middle income",
                "West Africa",
                "West Asia",
                "Western Europe",
                "World",
                "Low income",
            ]
        ).reset_index()

        all_countries = data_df["Entity"].tolist()
        country_list = list(dict.fromkeys(all_countries))

        return country_list

    def correlate_quantity(self):
        """Provides a correlation heatmap of the quantity columns"""

        correlation = self.data_df.iloc[:, 13:].corr()
        mask = np.zeros_like(correlation, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

        heatmap = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True, mask=mask)
        heatmap.set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)
        ax_figure = heatmap.axes
        ax_figure.text(
            0,
            -0.35,
            "Source: Agricultural total factor productivity (USDA), Our World in Data 2021",
            fontsize=12,
            ha="left",
            transform=heatmap.figure.transFigure,
        )

    def area_graph(self, country: str, normalize: bool):
        """
        Creates an area graph of the output of a given country or the whole world.
        It can be specified if the graph should show absolute numbers or relative numbers,
        where the yearly output is always 100%.
        The country input can either be empty or 'World' then the graph will show
        information for the whole world summarized, or it can be a country from the country_list.
        Then it will show the output for the specific country. If the input is something
        else, it will raise and error.

        Parameters
        ---------------
        country: string
            Defines if the data should be shown for a special country or for the whole world

        normalize: boolean
            Shows if graph should be normalized. Normalized means that it will be relative output
        """
        country_list = self.list_countries()

        # check if input for normalize is a boolean value
        if not isinstance(normalize, bool):
            raise TypeError("Variable 'normalize' is not a boolean.")

        # check if country input is World or none and adapt dataframe accordingly
        if country in ("World", None):
            country_df = self.data_df.groupby("Year", as_index=False).sum()
            # check if normalize is true and adapt dataframe accordingly
            if normalize is True:
                country_df["crop_output_quantity"] = (
                    country_df["crop_output_quantity"] / country_df["output_quantity"]
                )
                country_df["animal_output_quantity"] = (
                    country_df["animal_output_quantity"] / country_df["output_quantity"]
                )
                country_df["fish_output_quantity"] = (
                    country_df["fish_output_quantity"] / country_df["output_quantity"]
                )

        # check if country input is in country list
        elif country in country_list:
            country_df = self.data_df[self.data_df["Entity"] == f"{country}"]
            if normalize is True:
                country_df["crop_output_quantity"] = (
                    country_df["crop_output_quantity"] / country_df["output_quantity"]
                )
                country_df["animal_output_quantity"] = (
                    country_df["animal_output_quantity"] / country_df["output_quantity"]
                )
                country_df["fish_output_quantity"] = (
                    country_df["fish_output_quantity"] / country_df["output_quantity"]
                )

        # raise a value error if country input is invalid
        else:
            raise ValueError(f"{country} is not a valid country, try another one")

        # define colors to use in chart
        color_map = ["red", "steelblue", "green"]

        # create area chart
        plt.stackplot(
            country_df["Year"],
            country_df["crop_output_quantity"],
            country_df["animal_output_quantity"],
            country_df["fish_output_quantity"],
            labels=["Output Crop", "Output Animal", "Output Fish"],
            colors=color_map,
        )

        # add legend
        plt.legend(loc="upper left")

        # add axis labels
        plt.xlabel("Year")
        plt.ylabel("Quantity")

        # add title
        plt.title(f"{country}'s Output by Type of Crop, Animal, and Fish")

        # add source
        plt.text(
            0,
            -0.25,
            "Source: Agricultural total factor productivity (USDA), Our World in Data 2021",
            ha="left",
            transform=plt.gca().transAxes,
        )

        # display area chart
        plt.show()

    def area_graph(self, country: str, normalize: bool):
        """
        Creates an area graph of the output of a given country or the whole world.
        It can be specified if the graph should show absolute numbers or relative numbers,
        where the yearly output is always 100%.
        The country input can either be empty or 'World' then the graph will show
        information for the whole world summarized, or it can be a country from the country_list.
        Then it will show the output for the specific country. If the input is something
        else, it will raise and error.

        Parameters
        ---------------
        country: string
            Defines if the data should be shown for a special country or for the whole world

        normalize: boolean
            Shows if graph should be normalized. Normalized means that it will be relative output
        """
        country_list = self.list_countries()

        # check if input for normalize is a boolean value
        if not isinstance(normalize, bool):
            raise TypeError("Variable 'normalize' is not a boolean.")

        # check if country input is World or none and adapt dataframe accordingly
        if country in ("World", None):
            country_df = self.data_df.groupby("Year", as_index=False).sum()
            # check if normalize is true and adapt dataframe accordingly
            if normalize is True:
                country_df["crop_output_quantity"] = (
                    country_df["crop_output_quantity"] / country_df["output_quantity"]
                )
                country_df["animal_output_quantity"] = (
                    country_df["animal_output_quantity"] / country_df["output_quantity"]
                )
                country_df["fish_output_quantity"] = (
                    country_df["fish_output_quantity"] / country_df["output_quantity"]
                )

        # check if country input is in country list
        elif country in country_list:
            country_df = self.data_df[self.data_df["Entity"] == f"{country}"]
            if normalize is True:
                country_df["crop_output_quantity"] = (
                    country_df["crop_output_quantity"] / country_df["output_quantity"]
                )
                country_df["animal_output_quantity"] = (
                    country_df["animal_output_quantity"] / country_df["output_quantity"]
                )
                country_df["fish_output_quantity"] = (
                    country_df["fish_output_quantity"] / country_df["output_quantity"]
                )

        # raise a value error if country input is invalid
        else:
            raise ValueError(f"{country} is not a valid country, try another one")

        # define colors to use in chart
        color_map = ["red", "steelblue", "green"]

        # create area chart
        plt.stackplot(
            country_df["Year"],
            country_df["crop_output_quantity"],
            country_df["animal_output_quantity"],
            country_df["fish_output_quantity"],
            labels=["Output Crop", "Output Animal", "Output Fish"],
            colors=color_map,
        )

        # add legend
        plt.legend(loc="upper left")

        # add axis labels
        plt.xlabel("Year")
        plt.ylabel("Quantity")

        # display area chart
        plt.show()

    def compare_output(self, *country_input):
        """Plots the total of the output columns of selected countries.
        An unlimited number of countries can be selected for the comparison.

        Parameters
        ---------------
        country_list: string
            the countries selected for the comparison
        """

        input_list = list(country_input)

        for country_input in input_list:
            if type(country_input) is not str:
                raise TypeError("Country inputed is not a string")

        output_df = self.data_df[self.data_df["Entity"].isin(input_list)]

        sns.set_style("whitegrid")
        sns.lineplot(x="Year", y="output_quantity", hue="Entity", data=output_df)

        plt.title("Output Comparison for Selected Countries")
        plt.xlabel("Year")
        plt.ylabel("Output")
        plt.text(
            0,
            -0.25,
            "Source:Agricultural total factor productivity (USDA), Our World in Data 2021",
            ha="left",
            fontsize=10,
            transform=plt.gca().transAxes,
        )
        plt.show()

    def gapminder(self, year: int):
        """
        Generate a scatter plot for a specified ``year`` with the variables
        x being fertilizer quantity,
        y being output quantity,
        and the area of each dot being labor quantity.

        Parameters
        ----------
        year : int
            Scatter plot will display the data only for the specified year.
        """

        # check if year input is int
        if type(year) is not int:
            raise TypeError("Variable 'year' is not int.")

        # select subset of the dataframe that only contains rows for the selected year
        df_year = self.data_df[self.data_df["Year"] == year]

        # select subset of the dataframe that doesn't contain any regions
        country_list = self.list_countries()
        df_year_countries = df_year[df_year["Entity"].isin(country_list)]

        # get rowcount and raise exception if no entries were found for the year input
        if df_year_countries.shape[0] == 0:
            raise ValueError(
                "No entries were found for this year. Variable 'year' must be between 1961 and 2019"
            )
        # plot the bubble graph
        plt.figure(figsize=(10, 6))
        axis = sns.scatterplot(
            data=df_year_countries,
            x="fertilizer_quantity",
            y="output_quantity",
            size="labor_quantity",
            sizes=(100, 700),
            alpha=0.5,
        )
        axis.set(
            xlabel="Fertilizer Quantity (in tons)",
            ylabel="Output Quantity (in 1000$)",
            xscale="log",
            yscale="log",
            title=f"Fertilizer, Output and Labor Quantity in {year}",
        )
        plt.text(
            0,
            -0.15,
            "Source:Agricultural total factor productivity (USDA), Our World in Data 2021",
            ha="left",
            fontsize=10,
            transform=axis.transAxes,
        )
        plt.show()

    def choropleth(self, year: int):
        """Plots the total factor productivity of a selected year.
        Also, the function merges the data_df with the geopandas_df.

        Parameter
        ---------------
        year: int
            the year selected for the plot
        """

        if type(year) is not int:
            raise TypeError("Year must be an integer")

        self.geopandas_df.replace({"name": self.merge_dict}, inplace=True)
        merged_df = self.geopandas_df.merge(
            self.data_df, how="right", left_on="name", right_on="Entity"
        )
        merged_df.loc[merged_df["Year"] == year].plot(
            column="tfp",
            legend=True,
            figsize=[20, 10],
            legend_kwds={"label": "Total Factor Productivity"},
        )
        plt.title(f"Total Factor Productivity in {year}")
        plt.text(
            0,
            -0.25,
            "Source:Agricultural total factor productivity (USDA), Our World in Data 2021",
            ha="left",
            fontsize=10,
            transform=plt.gca().transAxes,
        )
