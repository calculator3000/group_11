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

        exists = os.path.isfile("../Downloads/download.csv")

        if not exists:
            response = requests.get(
                "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/"
                "Agricultural%20total%20factor%20productivity%20(USDA)"
                "/Agricultural%20total%20factor%20productivity%20(USDA).csv"
            )
            with open("../Downloads/download.csv", "wb") as file:
                file.write(response.content)

        self.data_df = pd.read_csv("../Downloads/download.csv")

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
