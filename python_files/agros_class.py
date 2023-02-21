import requests
import io
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Agros:
    """
    A class that downloads agricultural data and performs analysis on it. 
    
    Attributes
    ---------------
    data_df: Pandas Dataframe
        dataframe where the downloaded agricultural data can be loaded into. 
    
    
    Methods
    ---------------
    download_data
        downloads agricultural data from Githut, saves it to donwnlaod folder and creates Pandas DataFrame
        
    list_countries
        list all the available countires of the dataset
    
    """
    
    
    def __init__(self):
        self.data_df = pd.DataFrame