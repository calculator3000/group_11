def compare_output(*countries):
    """Plots the total of the output columns of selected countries

    Parameters
    ---------------
    country_list: string
        the countries selected for the comparison
    """

    country_list = list(countries)

    for country in country_list:
        if type(country) is not str:
            raise TypeError("Country inputed is not a string")

    data_df["total_outputs"] = (
        data_df["crop_output_quantity"]
        + data_df["animal_output_quantity"]
        + data_df["fish_output_quantity"]
    )

    df = data_df[data_df["Entity"].isin(country_list)]

    sns.set_style("whitegrid")
    sns.lineplot(x="Year", y="total_outputs", hue="Entity", data=df)

    plt.title("Output Comparison for Selected Countries")
    plt.xlabel("Year")
    plt.ylabel("Output")
    plt.show()
