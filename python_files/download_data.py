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

    self.geopandas_df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
