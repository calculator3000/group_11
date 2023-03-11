""" This module contains one class with the purpose of analyzing agricultural data internationally.
It contains seven methods. Those can download the data, list all the countries of the dataset,
provide a correlation matrix of the outputs, and plot an area chart of the agricultural output
of a choosen country.
It can also compare the output of choosen countries with a line graph, and plot a scatter plot
of fertilizer and output quantity.
Moreover, a choropleth of the total factor productivity for a selected year can be plotted.
Lastly, an ARIMA prediction for the total factor productivity is applied and the data
including the prediction is plotted.
"""

import warnings
import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from pmdarima.arima import auto_arima

warnings.filterwarnings("ignore")


class Agros:
    """
    A class that downloads agricultural data and performs analysis on it.

    Attributes
    ---------------
    data_df: Pandas Dataframe
        dataframe where the downloaded agricultural data can be loaded into

    merge_dict: dict
        a dictionary in order to change the spelling for some countries to allow merging

    geopandas_df: Geopandas df
        a geopandas dataframe where geo dataset with country-level polygons can be loaded into


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
        provides a choropleth plotting the total factor productivity of a selected year

    predictor
        applies an ARIMA prediction for the total factor productivity and
        plots the data including the prediction
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
        self.geopandas_df = gpd.GeoDataFrame

    def download_data(self):
        """
        Creates a 'downloads' folder, if it doesn't exist.
        Downloads agricultural data from Github repository and saves it to this folder,
        in case it is not already downloaded.
        It also creates Pandas Dataframe from the downloaded csv file.
        It also cleans the data so that aggregated rows (like Asia) are excluded.
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

        data_df = pd.read_csv("downloads/download.csv")
        countries_to_drop = [
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
        data_df = data_df.loc[~data_df["Entity"].isin(countries_to_drop)]
        self.data_df = data_df

        self.geopandas_df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    def list_countries(self):
        """Lists all the countries of the Entity column and removes the duplicates.

        Returns
        ---------------
        country_list: list
            All countries in the agros_data Entity column

        """

        country_list = list(self.data_df["Entity"].unique())

        return country_list

    def correlate_quantity(self):
        """Provides a correlation heatmap of the quantity columns"""

        correlation = self.data_df.loc[
            :, self.data_df.columns.str.contains("_quantity")
        ].corr()
        mask = np.zeros_like(correlation, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

        heatmap = sns.heatmap(
            correlation, vmin=-1, vmax=1, annot=True, mask=mask, cmap='coolwarm'
        )
        heatmap.set_title(
            "Correlation Heatmap of Output Columns", fontdict={"fontsize": 12}, pad=12
        )
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
            country_df = self.data_df.groupby("Year", as_index=False).sum().copy()
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
            country_df = self.data_df[self.data_df["Entity"] == f"{country}"].copy()
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

    def compare_output(self, *country_input: tuple):
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
                raise TypeError("Country inputted is not a string")
                
        for country_input in input_list:
            if country_input not in self.list_countries():
                raise ValueError("Country inputted not available in dataset")

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

        # get rowcount and raise exception if no entries were found for the year input
        if df_year.shape[0] == 0:
            raise ValueError(
                "No entries were found for this year. Variable 'year' must be between 1961 and 2019"
            )
        # plot the bubble graph
        plt.figure(figsize=(10, 6))
        axis = sns.scatterplot(
            data=df_year,
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
            
        if year < 1961 or year > 2019:
            raise ValueError(
                "No entries were found for this year. Variable 'year' must be between 1961 and 2019")

        self.geopandas_df.replace({"name": self.merge_dict}, inplace=True)
        merged_df = self.geopandas_df.merge(
            self.data_df, how="right", left_on="name", right_on="Entity"
        )
        merged_df.loc[merged_df["Year"] == year].plot(
            column="tfp",
            legend=True,
            figsize=[20, 10],
            vmin=50,
            vmax=250,
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

    def predictor(self, *countries: list):
        """
        Receives three countries and checks, which of them are included in the country_list.
        Then the rolling mean and the rolling standard deviation of tfp column of the data_df
        is being ploted for each country and the ARIMA model is used to predict the tfp for
        the next 30 year for each country.

        Parameters
        ---------------
        countries: list
        A list of three country names.

        """
        country_list = self.list_countries()

        # check for valid countries in input
        flat_list = [item for sublist in countries for item in sublist]
        invalid_countries = [x for x in flat_list if x not in country_list]

        if len(invalid_countries) > 0:
            print(f"Ignoring invalid countries: {', '.join(invalid_countries)}")

        valid_countries = [x for x in flat_list if x in country_list]
        print(valid_countries)

        if len(valid_countries) == 0:
            raise ValueError(
                "The list contains no valid countries. Available countries are: "
                + ", ".join(country_list)
            )

        # create lists to store data and predictions for each country
        data_list = []
        prediction_list = []

        # for loop to perform ARIMA prediction on all valid countries
        for country in valid_countries:
            # get dataset and set year to index in datetime format
            selected_data = self.data_df.loc[self.data_df["Entity"] == country]
            data = selected_data.set_index(selected_data.columns[1])
            data.index = pd.to_datetime(data.index, format="%Y")
            data_list.append(data)

            # plot the rolling mean and standard deviation to find out if the data is stationary
            plt.figure(figsize=(15, 7))
            plt.plot(data["tfp"], label="Original", color="orange")
            plt.plot(
                data["tfp"].rolling(window=12).mean(), color="red", label="Rolling mean"
            )
            plt.plot(
                data["tfp"].rolling(window=12).std(), color="green", label="Rolling std"
            )
            plt.xlabel("Date", fontsize=12)
            plt.ylabel("Total factor productivity", fontsize=12)
            plt.legend(loc="best")
            plt.title(
                "Prediction of future total factor productivity outputs with ARIMA: "
                + country
            )
            plt.text(
                0,
                -0.25,
                "Source:Agricultural total factor productivity (USDA), Our World in Data 2021",
                ha="left",
                fontsize=10,
                transform=plt.gca().transAxes,
            )

            # tune parameters for auto arima
            stepwise_fit = auto_arima(
                data["tfp"],
                start_p=1,
                start_q=0,
                max_p=10,
                max_q=10,
                m=1,
                start_P=0,
                seasonal=False,
                d=None,
                D=1,
                trace=True,
                error_action="ignore",  # Ignore incompatible settings
                suppress_warnings=True,
                stepwise=True,
            )

            # make prediction
            stepwise_fit.summary()
            prediction = pd.DataFrame(stepwise_fit.predict(n_periods=30))
            prediction_list.append(prediction)
            yhat = prediction[0]
            years = pd.Series(range(2021, 2051))
            xhat = pd.to_datetime(years, format="%Y")

            # add prediction to plot
            plt.plot(xhat, yhat, linestyle="dashed", color="orange")

        colors = ["red", "green", "blue"]
        plt.figure(figsize=(15, 7))
        for i in range(len(valid_countries)):
            data = data_list[i]
            prediction = prediction_list[i]
            yhat = prediction[0]
            years = pd.Series(range(2021, 2051))
            xhat = pd.to_datetime(years, format="%Y")
            plt.plot(data["tfp"], label=valid_countries[i], color=colors[i])
            plt.plot(xhat, yhat, linestyle="dashed", color=colors[i])
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Total factor productivity", fontsize=12)
        plt.legend(loc="best")
        plt.title(
            "Prediction of future total factor productivity outputs with ARIMA for all countries"
        )
        plt.text(
            0,
            -0.25,
            "Source:Agricultural total factor productivity (USDA), Our World in Data 2021",
            ha="left",
            fontsize=10,
            transform=plt.gca().transAxes,
        )
        plt.show()
