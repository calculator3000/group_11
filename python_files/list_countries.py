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
