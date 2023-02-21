"""[ ] Develop a sixth method that must be called gapminder.
This is a reference to the famous [gapminder tools]
(https://www.gapminder.org/tools/#$chart-type=bubbles&url=v1).
X This method should receive an argument year which must be an int.
X If the received argument is not an int, the method should raise a TypeError.
X This method should plot a scatter plot where
x is fertilizer_quantity, y is output_quantity,
TBA and the area of each dot should be a third relevant variable
you find with exploration of the data."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Downloads/download.csv")  # to be deleted


def gapminder(year: int):
    """
    Generate a scatter plot for a specified ``year`` with the variables
    x being fertilizer quantity,
    y being output quantity,
    and the area of each dot being ag land index.

    Parameters
    ----------
    year : int
        Scatter plot will display the data only for the specified year.
    """

    # maybe back to type since python thinks bool is int :-)
    if not isinstance(year, int):
        raise TypeError("Variable 'year' is not int.")

    df_year = df[df["Year"] == year]

    if df_year.shape[0] == 0:  # get rowcount
        raise ValueError(
            "No entries were found for this year. Variable 'year' must be between 1961 and 2019"
        )

    ax = sns.scatterplot(
        data=df_year, x="fertilizer_quantity", y="output_quantity", size="labor_index"
    )
    ax.set(
        xlabel="Fertilizer Quantity",
        ylabel="Output Quantity",
        xscale="log",
        yscale="log",
        title=f"Fertilizer and Output Quantity in {year}",
    )

    plt.show()


gapminder(1961)
gapminder(2019)
