import unittest
from finalproject import *
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import sys
import plotly.graph_objects as go
import plotly.express as px

###17 total assertions/calls to fail###

class TestPokemon(unittest.TestCase):

    def testDataAccess(self):
        
        #checking that website was accessed and scraped
        resp = requests.get('https://pokemondb.net/pokedex/squirtle').text

        soup = BeautifulSoup(resp, 'html.parser')
        table1 = soup.find_all(class_='resp-scroll')
        table = table1[0].find_all(class_='vitals-table')
        hp = int((table[0].find_all(class_='cell-num'))[0].string)
        tablenew = soup.find_all(class_='grid-col span-md-6 span-lg-4')
        heightraw = (tablenew[1].find_all(class_='vitals-table'))[0].find_all('td')[3].string
        height = float((heightraw.split('m'))[0])
        self.assertEqual(hp, 44)
        self.assertEqual(height, 0.5)

        #checking that data can be accessed from the cachefile
        with open('pokemon.json', 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        html = obj['https://pokemondb.net/pokedex/national']
        soup2 = BeautifulSoup(html, 'html.parser')
        section = soup2.find_all(class_='infocard')
        pokename = section[0].find_all(class_='ent-name')[0].text
        first_type = section[0].find_all('small')[1].find_all('a')[0].text
        self.assertEqual(pokename, 'Bulbasaur')
        self.assertEqual(first_type, 'Grass')

        #checking that data can be accessed from the database
        conn = sqlite3.connect('pokemon.db')
        cur = conn.cursor()
        sql = 'SELECT b.PokemonName, DexNumber from Pokemon JOIN Names as b ON b.Id = Pokemon.DexNumber'
        results = cur.execute(sql)
        result_list = results.fetchall()
        conn.close()

        self.assertEqual(result_list[1][0], 'Ivysaur')
        self.assertEqual(result_list[1][1], 2)


    def testStorage(self):

        #checking database storage information is correct        
        conn = sqlite3.connect('pokemon.db')
        cur = conn.cursor()
        sql = 'SELECT DexNumber from Pokemon'
        results = cur.execute(sql)
        result_list = results.fetchall()
        conn.close()

        self.assertIn((5,), result_list)
        self.assertEqual(len(result_list), 809)


        conn = sqlite3.connect('pokemon.db')
        cur = conn.cursor()
        sql = 'SELECT PokemonName, Id from Names'
        results2 = cur.execute(sql)
        result_list2 = results2.fetchall()
        conn.close()

        self.assertIn(('Pikachu', 25), result_list2)
        self.assertEqual(len(result_list2), 809)


    def testProcessing(self):
        
        #checking if classes processed correctly
        p1 = Pokemon('Bulbasaur', 1, 'Grass', 'Poison', 45, 49, 49, 65, 65, 45, 318, weight = 6.9, height = 0.7, male = 87.5, female = 12.5)
        p2 = Pokemon('Squirtle', 7, 'Water', 'None', 44, 48, 65, 50, 64, 43, 314, weight = 9.0, height = 0.5)
        list_of_commands = ['generation', '1']
        pokemon = [p1, p2]

        self.assertEqual(p1.name,"Bulbasaur")
        self.assertEqual(p2.first_type, "Water")
        self.assertEqual(p1.generation, '')


        #checking if data presentations processed data correctly to display graphs
        try:
            results = pie_chart(p1)
        except:
            self.fail()

        try:
            results = bar(pokemon, list_of_commands)
        except:
            self.fail()

        try:
            results = scatter(pokemon, list_of_commands)
        except:
            self.fail()

        try:
            results = table(p2)
        except:
            self.fail()


if __name__ == "__main__":
    unittest.main(verbosity=2)
