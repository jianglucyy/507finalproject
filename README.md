# Final Project for 507: Intermediate Programming

This project is an **interactive program** that gives you various information about a specific pokemon, specific type(s) of pokemon, specific generation of pokemon, or all pokemon. There are 4 simple data presentations, in the form of a pie chart, a bar graph, a scatter plot, and a table.

**Data sources used, including instructions for a user to access the data sources**
Crawling [and scraping] multiple pages in a site you haven’t used before - 8 Challenge Points
The website I used was https://pokemondb.net/pokedex/.
There are no API calls, and thus this project does not require any API keys.

**Any other information needed to run the program**
No extra information is needed to run the program. 

**Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.**
Order of my code, from beginning to end:
* Defined a class - Pokemon class, which I used to create the database as well as to process information for my data visualizations later. _Pokemon_ is initialized with the following attributes: 
    * name - the name of the pokemon (string)
    * number - the pokedex number of the pokemon (integer)
    * first_type - primary type of the pokemon (string)
    * second_type - secondary type of the pokemon or 'none' if doesn't have a secondary type (string)
    * hp - HP stat (integer)
    * attack - Attack stat (integer)
    * defense - Defense stat (integer)
    * spatk - Special Attack stat (integer)
    * spdef - Special Defense Stat (integer)
    * speed - Speed Stat (integer)
    * total - total of all stats added together (integer)
    * generation = '' - which generation the pokemon is from aka which series it was released in (integer)
    * male = 0.0 - male ratio of the pokemon species (float)
    * female = 0.0 - female ratio of the pokemon species (float)
    * height = 0.0 - height of the pokemon in meters (float)
    * weight = 0.0 - weight of the pokemon in kilograms (float)
* Created my cachefile/caching code
* Scraped the pages for the necessary information and created instances of all the Pokemon with their needed attributes
* Created 2 tables for my database and inserted the data from the cache
* Created functions for the four visualization methods:
    * pie_chart()
    * scatter()
    * table()
    * bar()
* Process commands and interactive prompt. The user first inputs the scope of the data they are looking at (single pokemon, one generation, one type, or all pokemon), and then the program will prompt the user through their possible options from there (the four visualizations, but not all four are available to each scope)

**Brief user guide, including how to run the program and how to choose presentation options**
Please look at the 'help.txt' file that is also in this repository for instructions. There are four beginning commands that the user can choose from, and then the program will show which data presentations the user can choose from there.

**Your GitHub repo must also contain a requirements.txt file that can be used by the teaching team to set up a virtual environment in which to run your project**
This can be found in the repository as well.
