def download_data():
    """
    Downloads agricultural data from Github repository and saves it to a download folder.
    Check if the file is already downloaded.
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

    data_df = pd.read_csv("../Downloads/download.csv")
    