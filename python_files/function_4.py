"""
tba
"""

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
        if country in ('World', None):
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