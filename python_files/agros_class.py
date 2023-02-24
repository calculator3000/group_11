""" This module contains one class with the purpose of analyzing agricultural data internationally.
It contains six methods. Those can download the data, list all the countries of the dataset,
provide a correlation matrix of the outputs, and plot an area chart of the agricultural output
of a choosen country.
It can also compare the output of choosen countries with a line graph, and plot a scatter plot
of fertilizer and output quantity.
"""

import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Agros:
    """
    A class that downloads agricultural data and performs analysis on it.

    Attributes
    ---------------
    data_df: Pandas Dataframe
        dataframe where the downloaded agricultural data can be loaded into.


    Methods
    ---------------
    download_data
        downloads agricultural data from Githut, saves it to donwnlaod folder
        and creates Pandas DataFrame

    list_countries
        list all the available countires of the dataset

    correlate_quantity
        provides a correlation heatmap of the quality columns

    compare_output
        Plots the output columns of selected countries
    """

    def __init__(self):
        self.data_df = pd.DataFrame

    def download_data(self):
        """
        Downloads agricultural data from Github repository and saves it to a download folder.
        Raises an error in case the file is already downloaded.
        It also creates Pandas Dataframe from the downloaded csv file.
        """

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

    def list_countries(self):
        """Lists all the countries of the Entity column and removes the duplicates.

        Returns
        ---------------
        country_list: list
            All countries in the agros_data Entity column

        """
        data_df_new_index = self.data_df.set_index("Entity")
        data_df_without_continents = data_df_new_index.drop(
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
            ]
        ).reset_index()

        all_countries = data_df_without_continents["Entity"].tolist()
        country_list = list(dict.fromkeys(all_countries))

        return country_list

    def correlate_quantity(self):
        """Provides a correlation heatmap of the quantitiy columns"""

        heatmap = sns.heatmap(
            self.data_df.iloc[:, 13:].corr(), vmin=-1, vmax=1, annot=True
        )
        heatmap.set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)

    def area_graph(self, country: str, normalize: bool):
        """
        Creates an area graph for a given country or the whole world. It can be specified if the
        graph should show absolute numbers or absolute numbers, where the yearly output is
        always 100%.

        Parameters
        ---------------
        country: string
            Defines if the data should be shown for a special country or for the whole world
        normalize: boolean
            Shows if graph should be normalized. Normalized means that it will be relative output.
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
        """Plots the total of the output columns of selected countries

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

        plt.show()
