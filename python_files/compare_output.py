def compare_output(*country_input):
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

    output_df = data_df[data_df["Entity"].isin(input_list)]

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
