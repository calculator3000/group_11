# Welcome to project Agros - Part 2
---
## Rules
1. Be sure that one member of the group submits [the link to the repo on moodle](https://moodle.novasbe.pt/mod/assign/view.php?id=277347).
2. We will pull the existing versions by 0:00 Tuesday, 14 March 2023. Remember: the pushes have a timestamp!

---
<div class="alert alert-danger">
    <b> NEVER USE USER PROMPTS, IT IS INFINITELY ANNOYING!! </b>
    <br>
    <b> Always use arguments for your methods.</b>
</div>


---
## Scenario (continuation)

Your company is participating in a two-day hackathon promoted to study the agricultural output of several countries. They send your group, the best team of Data Scientists in the company's roster. By undertaking this task, your company expects to contribute to the green transition by having a more savvy taskforce. You decide to create a python class for the challenge.

You spent the first day doing a lot of the code heavy lifting. It is now time to do some polishing. As you know your project might be picked up for an analysis presentation, you add an introduction about your group on the _README.md_ file. Be sure to add your **names**, **your student numbers** and **your e-mails**. It is time to add more features to the class so you can present the analysis in the showcase notebook.

## Goal

For this project, we will be using data from [Our World in Data](https://ourworldindata.org/). The dataset can be found [here](https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv). Be sure to take a look at the [data sictionary](https://github.com/owid/owid-datasets/blob/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/datapackage.json).

Use whatever python tools you find apropriate. We recommend seaborn for plottingm basic matplotlib, and geopandas for geographical data.

Day two is beginning.

### Day 2, Phase 1: Extending the scope

- [ ] Make sure you are not using aggregated columns. It makes no sense in using an Asian country and then also use *Asia* in your plots, for example. You did not notice this on day one (well, if you did, the real group, not the group from the scenario hackathon, congratulatios. Data Science is also about detail).
- [ ] ALL methods at the end of day 2 should have a descriptive title, correct labels, and an annotation stating the source of the data, like the **Source** in this [example](https://raw.githubusercontent.com/guimarais/iaea_reactors/main/Operations_Shutdowns.png). Don't lose time by formatting the rest of the plot, leave as is, but the source of the data is fundamental.


## Day 2, Phase 2: World view

- [ ] Make a module called **choropleth**. This method should receive a year as input, which must be an integer. **Raise** otherwise. We're going deep with our analysis and we're going to use geodata. We recommend you install geopandas. Alter the method where you download the data to also download and read a geographical dataset. The geo dataset must have the polygons for as many countries as possible. You can get such a datafile [here](https://www.naturalearthdata.com) (use cultural data, as it refers to countries). If you download a zip file, remember you want to access the shapefile (.shp) inside. [Read the documentation for geopandas for examples on how to read data](https://geopandas.org/en/stable/docs/user_guide/io.html).
- [ ] **Merge** (pandas equivalent to SQL JOIN) the agricultural data with the geodata on the countries. Make sure the **left** dataframe is the geopandas dataframe. When you plot the result of the merge, you may notice some important country or countries missing. That is because their names don't match. Make a **VARIABLE** of the class called *merge_dict* which is a dictionary that renames at least one country
- [ ] Plot the **tfp** variable on a world map. Make sure you use a colorbar. [This example should help](https://medium.com/geekculture/three-ways-to-plot-choropleth-map-using-python-f53799a3e623).

<div class="alert alert-danger">
    <b> Treat the geopandas dataframe as a regular dataframe. </b>
    <br>
    <b> Keep the "geometry" column untouched, as that is the special column for plots.</b>
</div>




### Day 2, Phase 3: Predictor

- [ ] Make a **predictor** method that receives a list of countries as input, up to three. If one or more countries on the list is not present in the Agricultural dataframe, it should be ignored. If none is, **raise** an error message reminding the user what countries are available. Maybe you already have that from yesterday?
- [ ] The **predictor** method should plot the **tfp** in the dataset and then complement it with an **ARIMA** prediction up to 2050. Use the same color for each country's actual and predicted data, but a different line style.

### Day 2, Phase 4: Cleaning up

- [ ] Add a yaml file to git with all the packages you used, a conda environment file. This file will be used to generate an environment where your code will be ran. Remember to make it OS independent.
- [ ] Use sphinx to generate a __docs__ directory that will shocase the documentation of your code. Remember to comment .gitignore appropriately so everything is included. Update README.md to tell the user how to start using the project.

___
### Finishing up:

Let's begin by telling a story.

Start by an overall analysis with the gapminder plot for the most recent year and the year 1980. What can you see as the major changes regarding the variables you considered the most relevant on day 1?

Choose **three** countries in the list. Any countries will do, but at least one must be a member of the EU and one must be outside the EU.  
Use all other analysis methods (all you have developed except the **gapminder**, the **choropleth**, and the **predictor**) to analyse the evolution of each country's agricultural data. Write a small story about it.

End by showing **choropleth** for the most recent year and 2000.

Finish by analysing the output of **predictor**.

---
## Grading

Between the two parts, there are 20 gradable items in both Part 1 and 2. The last two items of Day 1, Phase 1 are not gradable.

<div class="alert alert-danger">
    <b> REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS, BUT THE FINAL CLASS MUST BE IN A SINGLE .py FILE! </b>
    <br>
    <b> The final delivery of the project is the "showcase" notebook. Don't place this notebook together with prototyping notebooks.</b>
    <br>
    <b> Prototyping notebooks must have their own separate directory.</b>
    <br>
    <b> We will only consider contents in your "master" repository before the end of the deadline.</b>
</div>
