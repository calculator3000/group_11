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
