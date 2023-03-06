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
        column="tfp",  # Assign numerical data column
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
