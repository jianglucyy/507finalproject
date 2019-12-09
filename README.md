# 507finalproject
Final Project for 507: Intermediate Programming

This project is an **interactive program** that gives you various information about a specific pokemon, specific type(s) of pokemon, specific generation of pokemon, or all pokemon. There are 4 simple data presentations, in the form of a pie chart, a bar graph, a scatter plot, and a table.

**Data sources used, including instructions for a user to access the data sources**
Crawling [and scraping] multiple pages in a site you haven’t used before - 8 Challenge Points
The website I used was https://pokemondb.net/pokedex/.
There are no API calls, and thus this project does not require any API keys.

**Any other information needed to run the program**
No extra information is needed to run the program. 

**Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.**
Order of my code, from beginning to end:
* I start with defining a Pokemon class, which I used to create the database as well as to process information for my data visualizations later._Pokemon_ is initialized with the following attributes: 
    * name, number, first_type, second_type, hp, attack, defense, spatk, spdef, speed, total, generation = '', male = 0.0, height = 0.0, weight = 0.0, female = 0.0
* I have my cachefile/cache creation
* I scrape the pages for the necessary information and created instances of all the Pokemon with their needed attributes
* created 2 tables for my database and inserted the data from the cache
* created functions for the four visualization methods:
    * pie_chart()
    * scatter()
    * table - table()
    * bar()
* The last section is my process commands and interactive prompt. The user first inputs the scope of the data they are looking at (single pokemon, one generation, one type, or all pokemon), and then the program will prompt the user through their possible options from there (the four visualizations, but not all four are available to each scope)

**Brief user guide, including how to run the program and how to choose presentation options**
Please look at the 'help.txt' file that is also in this repository.

**Your GitHub repo must also contain a requirements.txt file that can be used by the teaching team to set up a virtual environment in which to run your project**
This can be found in the repository as well.
