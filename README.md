# Project Agros: analysis of the world’s agricultural output

## Description
The repository contains our advanced programming group project, using data on agriculture by Our World in Data, analyzing the world’s agricultural production between the years 1961 and 2019. The goal is to contribute to the green transition.

The project is part of the Advanced Programming Course at Nova SBE. Our main analysis can be found in the showcase Jupyter Notebook. Here, the agricultural evolution of several countries is analyzed with a comparison of the outputs, a gapminder plot, a correlation matrix, area graphs, a choropleth map, and finalized with a prediction of the countries' outputs. 

The project is shared work by Group 11:\
Julia Stieler - 56040, 56040@novasbe.pt\
Hannah Dickescheid - 50178, 50178@novasbe.pt\
Carlos Ferrufino - 53276, 53276@novasbe.pt\
Eva Zinser - 53100, 53100@novasbe.pt


## Data
We are using data on Agricultural total factor productivity (USDA), downloaded from Our World in Data, (datasource can be found [here](https://github.com/owid/owid-datasets/tree/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)))

The original data was published by the United States Department for Agriculture (USDA) Economic Research Service.


## Getting started
1. The environment was saved in the file ```agrosenv.yml```\.
To learn how to use the environment, follow the documentation found [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

2. Documentation was built using sphinx. 
To view it, open ```docs/_build/html/index.html```.

3. Our repository is structured like this: In the main directory, you can find our showcase notebook ```showcase_notebook.ipynb```. It contains an analysis of the data and shows our findings. For the project, a class with several methods was created. All methods used belong to this class. The file ```agros_class.py``` containing the class can be found in the python_files directory. 

4. Run the ```download_data``` method first. It will download the agricultural data from Github and save it to a folder called ```downloads```.

## Agros Class
The class is PEP8 compliant, using black and pylint.

```Agros``` has several methods.\
Those can download the data, list all the countries of the dataset,provide a correlation matrix of the outputs, and plot an area chart of the agricultural output of a choosen country. It can also compare the output of choosen countries with a line graph, and plot a scatter plot
of fertilizer and output quantity. Moreover, a choropleth of the total factor productivity for a selected year can be plotted.

## License
GPL-3.0 license

## Project Status
End Sprint :)

## Special Thanks 
to Luis and Our World In Data
