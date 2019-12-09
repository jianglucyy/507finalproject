import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import sys
import plotly.graph_objects as go
import plotly.express as px

#each pokemon will have the following attributes. Will be used to create the database as well as to generate the data visualizations later.
class Pokemon:
    def __init__(self, name, number, first_type, second_type, hp, attack, defense, spatk, spdef, speed, total, generation = '', male = 0.0, height = 0.0, weight = 0.0, female = 0.0):
        self.name = name
        self.number = number
        self.generation = generation
        self.first_type = first_type
        self.second_type = second_type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.speed = speed
        self.total = total
        self.male = male
        self.female = female
        self.height = height
        self.weight = weight


#scraped pages are cached in this file
CACHE_FNAME = 'pokemon.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_unique_key(baseurl):
    return baseurl

def make_request_using_cache(baseurl):
    unique_ident = get_unique_key(baseurl)
    myurl = baseurl
        ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(myurl)
        #CACHE_DICTION[unique_ident] = json.loads(resp.text)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#first scrape is the main pokedex page where I scrape the pokemon names and types as well as the addres to crawl to each individual pokemon's page
# URL = 'https://pokemondb.net/pokedex/national'
# html = make_request_using_cache(URL)
# soup = BeautifulSoup(html, 'html.parser')

# section = soup.find_all(class_='infocard')
# pokemonClass = []

# for each in section:
#     #getting the pokemon name and types
#     pokename = each.find_all(class_='ent-name')[0].text
#     first_type = (each.find_all('small')[1]).find_all('a')[0].text
#     try:
#         second_type = (each.find_all('small')[1]).find_all('a')[1].text
#     except:
#         second_type = 'None'


#     #getting the individual pokemon urls
#     num = int(((each.find_all(class_='infocard-lg-data text-muted'))[0].find('small').string)[1:])
#     pokepage = each.find('a')['href']
#     URL2 = 'https://pokemondb.net' + pokepage

#     #fetching data from each individual pokemon's page
#     html2 = make_request_using_cache(URL2)
#     soup2 = BeautifulSoup(html2, 'html.parser')
#     table1 = soup2.find_all(class_='resp-scroll')
#     table = table1[0].find_all(class_='vitals-table')

#     #getting all of the Pokemon stats
#     hp = int((table[0].find_all(class_='cell-num'))[0].string)
#     attack = int((table[0].find_all(class_='cell-num'))[3].string)
#     defense = int((table[0].find_all(class_='cell-num'))[6].string)
#     spatk = int((table[0].find_all(class_='cell-num'))[9].string)
#     spdef = int((table[0].find_all(class_='cell-num'))[12].string)
#     speed = int((table[0].find_all(class_='cell-num'))[15].string)
#     total = int((table[0].find_all(class_='cell-total'))[0].find('b').text)

#     #getting heights
#     tablenew = soup2.find_all(class_='grid-col span-md-6 span-lg-4')
#     allheights = []
#     heightraw = (tablenew[1].find_all(class_='vitals-table'))[0].find_all('td')[3].string
#     height = float((heightraw.split('m'))[0])
#     allheights.append(height)

#     #getting weights
#     allweights = []
#     weightraw = (tablenew[1].find_all(class_='vitals-table'))[0].find_all('td')[4].string
#     weight = float((weightraw.split('kg'))[0])
#     allweights.append(weight)

#     #getting the genders
#     tablegender = soup2.find_all(class_='grid-col span-md-6 span-lg-12')
#     try:
#         maleraw = (tablegender[1].find_all(class_='vitals-table'))[0].find_all('span')[0].text
#         male = float((maleraw.split('%'))[0])
#         femaleraw = (tablegender[1].find_all(class_='vitals-table'))[0].find_all('span')[1].text
#         female = float((femaleraw.split('%'))[0])  
#     except:
#         #this is going to be used to differentiate pokemon that are genderless
#         male = 555.0
#         female = 555.0

#     #creating all of the Pokemon
#     pokeMON = Pokemon(name = pokename, number = num, first_type = first_type, second_type = second_type, hp = hp, attack = attack, defense = defense, spatk = spatk, spdef = spdef, speed = speed, total = total, height = height, weight = weight, male = male, female = female)
#     pokemonClass.append(pokeMON)


#to insert generations for each Pokemon
def poke_generation():
    for p in pokemonClass:
        if p.number <= 151:
            p.generation = 1
        elif p.number <= 251:
            p.generation = 2
        elif p.number <= 386:
            p.generation = 3
        elif p.number <= 493:
            p.generation = 4
        elif p.number <= 649:
            p.generation = 5        
        elif p.number <= 721:
            p.generation = 6
        elif p.number <= 809:
            p.generation = 7
        elif p.number <= 890:
            p.generation = 8
        else:
            print('new pokemon???')

# poke_generation()

#creating the tables
def init_db():
    conn = sqlite3.connect("pokemon.db")

    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS 'Pokemon';""")
    cur.execute("""DROP TABLE IF EXISTS 'Names';""")

    cur.execute("""CREATE TABLE Names(
    Id integer PRIMARY KEY AUTOINCREMENT,
    PokemonName text
    )""")
    conn.commit()

    cur.execute("""CREATE TABLE Pokemon(
    DexNumber integer PRIMARY KEY,
    Generation integer,
    Type1 text,
    Type2 text,
    HP integer,
    Attack integer,
    Defense integer,
    SpAtk integer,
    SpDef integer,
    Speed integer,
    Total integer,
    Height real,
    Weight real,
    MaleRatio real,
    FemaleRatio real,
    FOREIGN KEY(DexNumber) REFERENCES Names(Id)
    )""")
    conn.commit()

# init_db()  


#inserting into the names table and pokemon table
def insert_names():
    conn = sqlite3.connect('pokemon.db')
    cur = conn.cursor()

    for poke in pokemonClass:
        cur.execute("""insert into names values (?,?)""", [None, poke.name])
    conn.commit()
    conn.close()

# insert_names()

def insert_pokes():
    conn = sqlite3.connect('pokemon.db')
    cur = conn.cursor()

    for poke in pokemonClass:
        cur.execute("""insert into pokemon values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [poke.number, poke.generation, poke.first_type, poke.second_type, poke.hp, poke.attack, poke.defense, poke.spatk, poke.spdef, poke.speed, poke.total, poke.height, poke.weight, poke.male, poke.female])
    conn.commit()
    conn.close()

# insert_pokes()



#for creating pie chart of gender ratios of an individual pokemon
def pie_chart(pokemon):
    
    if pokemon.male == 555.0:
        #accounting for genderless pokemon mentioned earlier
        fig = go.Figure(data=[go.Pie(labels=['Genderless'], values=[100])])
        fig.update_traces(hoverinfo='label+percent')
        fig.show()
    else:
        #and the rest of the pokemon with genders
        labels = ['Male','Female']
        values = [pokemon.male, pokemon.female]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent')
        fig.update_layout(title_text="Gender Ratio for " + pokemon.name)
        fig.show()


#for creating the scatter of height and weight of pokemon
def scatter(list_of_pokes, list_of_commands):
    weights = []
    heights = []
    names = []
    for each in list_of_pokes:
        weights.append(each.weight)
        heights.append(each.height)
        names.append(each.name)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weights, y=heights, mode="markers", hovertext=names))
    capitalize = list_of_commands[0].capitalize()

    if len(list_of_pokes) == 809:
        fig.update_layout(title = 'Height and Weight Scatter Plot for All Pokémon', xaxis_title='Weight (kg)', yaxis_title='Height (m)')
    else:
        fig.update_layout(title = 'Height and Weight Scatter Plot for ' + capitalize + " " + list_of_commands[1].capitalize() + ' Pokémon', xaxis_title='Weight (kg)', yaxis_title='Height (m)')
    fig.update_yaxes(tick0=0.0)
    fig.update_xaxes(tick0=0.0)
    fig.show()


#creating the table to show pokemon stats
def table(pokemon):
    fig = go.Figure(data=[go.Table(header=dict(values=[pokemon.name, 'Stats']), cells=dict(values=[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Defense', 'Speed', 'Total'], [pokemon.hp, pokemon.attack, pokemon.defense, pokemon.spatk, pokemon.spdef, pokemon.speed, pokemon.total]]))])
    fig.show()


#creating the bar graphs for types of pokemon
def bar(list_pokes, list_of_commands):
    normal = []
    fighting =[]
    flying = []
    poison = []
    ground = []
    rock = []
    bug = []
    ghost = []
    steel = []
    fire = []
    water = []
    grass = []
    electric = []
    psychic = []
    ice = []
    dragon = []
    dark = []
    fairy = []
    for each in list_pokes:
        if each.first_type == 'Normal':
            normal.append(each)
        elif each.first_type == 'Fighting':
            fighting.append(each)
        elif each.first_type == 'Flying':
            flying.append(each)
        elif each.first_type == 'Poison':
            poison.append(each)
        elif each.first_type == 'Ground':
            ground.append(each)
        elif each.first_type == 'Rock':
            rock.append(each)
        elif each.first_type == 'Bug':
            bug.append(each)
        elif each.first_type == 'Ghost':
            ghost.append(each)   
        elif each.first_type == 'Steel':
            steel.append(each)
        elif each.first_type == 'Fire':
            fire.append(each)
        elif each.first_type == 'Water':
            water.append(each)
        elif each.first_type == 'Grass':
            grass.append(each)
        elif each.first_type == 'Electric':
            electric.append(each)
        elif each.first_type == 'Psychic':
            psychic.append(each)
        elif each.first_type == 'Ice':
            ice.append(each)
        elif each.first_type == 'Dragon':
            dragon.append(each)
        elif each.first_type == 'Dark':
            dark.append(each)
        elif each.first_type == 'Fairy':
            fairy.append(each)
        else:
            print(each.first_type)

        if each.second_type == 'Normal':
            normal.append(each)
        elif each.second_type == 'Fighting':
            fighting.append(each)
        elif each.second_type == 'Flying':
            flying.append(each)
        elif each.second_type == 'Poison':
            poison.append(each)
        elif each.second_type == 'Ground':
            ground.append(each)
        elif each.second_type == 'Rock':
            rock.append(each)
        elif each.second_type == 'Bug':
            bug.append(each)
        elif each.second_type == 'Ghost':
            ghost.append(each)   
        elif each.second_type == 'Steel':
            steel.append(each)
        elif each.second_type == 'Fire':
            fire.append(each)
        elif each.second_type == 'Water':
            water.append(each)
        elif each.second_type == 'Grass':
            grass.append(each)
        elif each.second_type == 'Electric':
            electric.append(each)
        elif each.second_type == 'Psychic':
            psychic.append(each)
        elif each.second_type == 'Ice':
            ice.append(each)
        elif each.second_type == 'Dragon':
            dragon.append(each)
        elif each.second_type == 'Dark':
            dark.append(each)
        elif each.second_type == 'Fairy':
            fairy.append(each)
        else:
            print('new type???')

    types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
    numbers = [len(normal), len(fighting), len(flying), len(poison), len(ground), len(rock), len(bug), len(ghost), len(steel), len(fire), len(water), len(grass), len(electric), len(psychic), len(ice), len(dragon), len(dark), len(fairy)]
    fig = go.Figure([go.Bar(x=types, y=numbers)])
    
    if list_of_commands[0] == 'all':
        fig.update_yaxes(tick0=0, dtick=10)
        fig.update_layout(title="Number of Each Pokémon type in All Generations", xaxis_title="Type of Pokémon", yaxis_title="Number of Pokémon")
    else:    
        fig.update_yaxes(tick0=0, dtick=2)
        fig.update_layout(title="Number of Each Pokémon type in Generation " + list_of_commands[1], xaxis_title="Type of Pokémon", yaxis_title="Number of Pokémon")
    fig.show()


#to get user input
def get_question():
    return input()


#where all of the user inputs are processed to get the right output
def process_command(command):
    conn = sqlite3.connect('pokemon.db')
    cur = conn.cursor()

    list_of_commands = command.split(' ')
    if list_of_commands[0] == 'pokemon':
        try:
            query = list_of_commands[1].capitalize()
            sql_code = 'SELECT b.PokemonName, Type1, Type2, HP, Attack, Defense, SpAtk, SpDef, Speed, [Total], MaleRatio, FemaleRatio, DexNumber  FROM Pokemon JOIN Names as b ON Pokemon.DexNumber = b.Id WHERE b.PokemonName = '
            sql_code += "'" + query + "'"
            cur.execute(sql_code)
            result = cur.fetchall()
            if len(result) == 0:
                print('Pokémon not found. Check your spelling\n')
            else:
                for each in result:
                    pokemon = Pokemon(name = query, number = each[12], first_type = each[1], second_type = each[2], hp = each[3], attack = each[4], defense = each[5], spatk = each[6], spdef = each[7], speed = each[8], total = each[9], male = each[10], female = each[11])

                print('\nPlease select one of the options below for ' + query + ':')
                print('1. View Stats')
                print('2. View Gender Ratio')
                response = ''
                
                while response != '1' and response != '2' and response != '3' and response !='exit':
                    response = get_question()
                    if response == '1':
                        table(pokemon)
                    elif response == '2':
                        pie_chart(pokemon)
                    elif response =='exit':
                        pass
                    else:
                        print ("Please input 1 or 2:")

                conn.commit()
                conn.close()
                return result
        except:
            print('Please input a Pokémon Name too\n')


    elif list_of_commands[0] == 'generation':
        try:
            query = list_of_commands[1]
            sql_code = 'SELECT b.PokemonName, Type1, Type2, HP, Attack, Defense, SpAtk, SpDef, Speed, [Total], MaleRatio, FemaleRatio, DexNumber, Height, Weight  FROM Pokemon JOIN Names as b ON Pokemon.DexNumber = b.Id WHERE Generation = '
            sql_code += query
            cur.execute(sql_code)
            result = cur.fetchall()
            generation_pokemon = []
            for each in result:
                pokemon = Pokemon(name = each[0], number = each[12], first_type = each[1], second_type = each[2], hp = each[3], attack = each[4], defense = each[5], spatk = each[6], spdef = each[7], speed = each[8], total = each[9], male = each[10], female = each[11], height = each[13], weight = each[14])
                generation_pokemon.append(pokemon)
            if len(generation_pokemon) == 0:
                print('Please enter a valid generation\n')
            else:
                print('\nPlease select one of the options below for generation ' + query +' Pokémon:')
                print('1. View Average Stats')
                print('2. View Type Breakdown')
                print('3. View Scatter of Height and Weight')
                response = ''
                    #print('happy')

                while response != '1' and response != '2' and response != '3' and response !='exit':
                    response = get_question()
                    if response == '1':
                        total_hp = 0
                        total_attack = 0
                        total_defense = 0
                        total_spatk = 0
                        total_spdef = 0
                        total_speed = 0
                        total_total = 0
                        for each in generation_pokemon:
                            total_hp += each.hp
                            total_attack += each.attack
                            total_defense += each.defense
                            total_spatk += each.spatk
                            total_spdef += each.spdef
                            total_speed += each.speed
                            total_total += each.total
                        hp = round(total_hp/len(generation_pokemon), 1)
                        attack = round(total_attack/len(generation_pokemon), 1)
                        defense = round(total_defense/len(generation_pokemon), 1)
                        spatk = round(total_spatk/len(generation_pokemon), 1)
                        spdef = round(total_spdef/len(generation_pokemon), 1)
                        speed = round(total_speed/len(generation_pokemon), 1)
                        total = round(total_total/len(generation_pokemon), 1)

                        average_pokemon = Pokemon(name = 'Generation ' + query + ' Pokémon Averages', number = 0, first_type = 'none', second_type = 'none', hp = hp, attack = attack, defense = defense, spatk = spatk, spdef = spdef, speed = speed, total = total)
                        table(average_pokemon)
                    elif response == '2':
                        bar(generation_pokemon, list_of_commands)
                    elif response == '3':
                        scatter(generation_pokemon, list_of_commands)
                    elif response =='exit':
                        pass
                    else:
                        print ("Please input 1, 2, or 3:")
            conn.commit()
            conn.close()
            return result
        except:
            print('Please enter a generation number too\n')


    elif list_of_commands[0] == 'all':
        if len(list_of_commands) != 1:
            print('all does not have other parameters\n')
        else:
            sql_code = 'SELECT b.PokemonName, Type1, Type2, HP, Attack, Defense, SpAtk, SpDef, Speed, [Total], MaleRatio, FemaleRatio, DexNumber, Height, Weight  FROM Pokemon JOIN Names as b ON Pokemon.DexNumber = b.Id'
            cur.execute(sql_code)
            result = cur.fetchall()
            all_pokemon = []
            for each in result:
                pokemon = Pokemon(name = each[0], number = each[12], first_type = each[1], second_type = each[2], hp = each[3], attack = each[4], defense = each[5], spatk = each[6], spdef = each[7], speed = each[8], total = each[9], male = each[10], female = each[11], height = each[13], weight = each[14])
                all_pokemon.append(pokemon)

            print('\nPlease select one of the options below for all Pokémon:')
            print('1. View Average Stats')
            print('2. View Type Breakdown')
            print('3. View Scatter of Height and Weight')
            response = ''
            
            while response != '1' and response != '2' and response != '3' and response !='exit':
                response = get_question()
                if response == '1':
                    total_hp = 0
                    total_attack = 0
                    total_defense = 0
                    total_spatk = 0
                    total_spdef = 0
                    total_speed = 0
                    total_total = 0
                    for each in all_pokemon:
                        total_hp += each.hp
                        total_attack += each.attack
                        total_defense += each.defense
                        total_spatk += each.spatk
                        total_spdef += each.spdef
                        total_speed += each.speed
                        total_total += each.total
                    hp = round(total_hp/len(all_pokemon), 1)
                    attack = round(total_attack/len(all_pokemon), 1)
                    defense = round(total_defense/len(all_pokemon), 1)
                    spatk = round(total_spatk/len(all_pokemon), 1)
                    spdef = round(total_spdef/len(all_pokemon), 1)
                    speed = round(total_speed/len(all_pokemon), 1)
                    total = round(total_total/len(all_pokemon), 1)

                    average_pokemon = Pokemon(name = 'All Pokémon Averages', number = 0, first_type = 'none', second_type = 'none', hp = hp, attack = attack, defense = defense, spatk = spatk, spdef = spdef, speed = speed, total = total)
                    table(average_pokemon)
                elif response == '2':
                    bar(all_pokemon, list_of_commands)
                elif response == '3':
                    scatter(all_pokemon, list_of_commands)
                elif response =='exit':
                    pass
                else:
                    print ("Please input 1, 2, or 3:")
            conn.commit()
            conn.close()
            return result

    elif list_of_commands[0] == 'type':
        try:
            query = list_of_commands[1]
            sql_code = 'SELECT b.PokemonName, Type1, Type2, HP, Attack, Defense, SpAtk, SpDef, Speed, [Total], MaleRatio, FemaleRatio, DexNumber, Height, Weight  FROM Pokemon JOIN Names as b ON Pokemon.DexNumber = b.Id WHERE Type1 == '
            query = query.capitalize()
            sql_code += "'" + query + "'" 'or Type2 == ' + "'" + query + "'"
            cur.execute(sql_code)
            result = cur.fetchall()
            type_pokemon = []
            for each in result:
                pokemon = Pokemon(name = each[0], number = each[12], first_type = each[1], second_type = each[2], hp = each[3], attack = each[4], defense = each[5], spatk = each[6], spdef = each[7], speed = each[8], total = each[9], male = each[10], female = each[11], height = each[13], weight = each[14])
                type_pokemon.append(pokemon)

            if len(type_pokemon) == 0:
                print('No Pokémon found. Check your spelling\n')
            else:
                print('\nPlease select one of the options below for ' + query + ' Type Pokémon:')
                print('1. View Average Stats')
                print('2. View Scatter of Height and Weight')
                

                response = ''
                

                while response != '1' and response != '2' and response !='exit':
                    response = get_question()
                    if response == '1':
                        total_hp = 0
                        total_attack = 0
                        total_defense = 0
                        total_spatk = 0
                        total_spdef = 0
                        total_speed = 0
                        total_total = 0
                        for each in type_pokemon:
                            total_hp += each.hp
                            total_attack += each.attack
                            total_defense += each.defense
                            total_spatk += each.spatk
                            total_spdef += each.spdef
                            total_speed += each.speed
                            total_total += each.total
                        hp = round(total_hp/len(type_pokemon), 1)
                        attack = round(total_attack/len(type_pokemon), 1)
                        defense = round(total_defense/len(type_pokemon), 1)
                        spatk = round(total_spatk/len(type_pokemon), 1)
                        spdef = round(total_spdef/len(type_pokemon), 1)
                        speed = round(total_speed/len(type_pokemon), 1)
                        total = round(total_total/len(type_pokemon), 1)

                        average_pokemon = Pokemon(name = 'All ' + query + ' Type Pokémon Averages', number = 0, first_type = 'none', second_type = 'none', hp = hp, attack = attack, defense = defense, spatk = spatk, spdef = spdef, speed = speed, total = total)
                        table(average_pokemon)
                    elif response == '2':
                        scatter(type_pokemon, list_of_commands)
                    elif response =='exit':
                        pass
                    else:
                        print('Please input 1 or 2: ')
            conn.commit()
            conn.close()
            return result               
        except:
            print('Please enter a Pokémon Type too\n')

    elif list_of_commands[0] == 'exit':
        sys.exit('Bye!')
    else:
        (print('Command not recognized: ' + str(command) + "\n"))

#help document
def load_help_text():
    with open('help.txt') as f:
        return f.read()

#create interactive part
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command or "help" for options: ')

        if response == 'help':
            print(help_text)
        else:
            process_command(response)

    sys.exit("Bye!")

if __name__ == "__main__":
    interactive_prompt()









