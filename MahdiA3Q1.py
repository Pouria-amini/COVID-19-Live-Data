"""
        [===============================================================================================]
        [                                                                                               ]
        [                         Assignment NO: 3                                                      ]
        [                         Question NO: 1                                                        ]
        [                         Author: Mahdi Amini                                                   ]
        [                         P.Con: Getting data from the internet and read and write csv file     ]
        [                                and displaying some visualisations.                            ]
        [                         Date Started: 22-04-2020                                              ]
        [                         Date Finished: 25-04-2020                                             ]
        [                         ICS3UI-02 for Ms. Harris                                              ]
        [                                                                                               ]
        [-----------------------------------------------------------------------------------------------]
        [                                 Program Description                                           ]
        [                                                                                               ]
        [   This program Gets the information regarding coronavirus from www.worldometers website and s-]
        [ave them into a CSV file. The next thing this program provides us with is the maps of each type]
        [of the data like total cases, total death and etc. This program also creates a diagram and sav-]
        [es. All of these data will be saved into "data & map" directory and you can refer them any time]
        [you want. The thing that should be notice is that 'every time you run the program, all data,   ]
        [including pie chart image, maps and CSV data will be refreshed according to the live data on t-]
        [he website'. If you are running the program for the first and there is no file in the data &   ]
        [map directory, all these data will be created after you run the program. Make sure to run the  ]
        [maps on a "Browser" like Firefox, Chrome, Safari or etc.
        [                                                                                               ]
        [-----------------------------------------------------------------------------------------------]
        [                                           Sources                                             ]
        [                                                                                               ]
        [    1-"Coronavirus Data from:"                                                                 ]
        [         https://www.worldometers.info/coronavirus/#countries                                  ]
        [                                                                                               ]
        [    2-"how to create Choropleth map and pie chart from : Folium and Matplot documentation"     ]
        [                                                                                               ]
        [===============================================================================================]

       ***
       This Assignment consist of 1 py File (MahdiA3Q1) and a json file into data & map directory (Countries.json)
       After running the program, 6 files will be added to the data & map directory.
       ***

       ##################### To run this program make sure you are connected to the INTERNET ########################
"""
from bs4 import BeautifulSoup

import requests

import pandas as pd

import os

import folium

import csv

import json

import matplotlib.pyplot as plt

import datetime


def Coronavirus_Choropleth_map(territories, name, data, legend_name, color_brewer):
    """ This Function Creates Choropleth map for any data of the coronavirus"""

    # The Choropleth map of New Cases in the time you run the code
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='OpenStreetMap')  # setting the starting point
    folium.Choropleth(
        geo_data=territories,  # The territories Data
        name=name,  # The name of the map
        data=data,  # The Coronavirus Data
        columns=['Country', legend_name],  # Using the columns of Country and New Cases in the csv data
        key_on='feature.properties.name',  # Using the name in the territories data
        fill_color=color_brewer,  # Setting its COLOR BREWER
        fill_opacity=0.7,  # Setting the boundaries
        line_opacity=0.2,  # Setting the boundaries
        legend_name='Coronavirus ' + legend_name + ' on: ' + str(datetime.date.today())  # The name of the legend
    ).add_to(m)
    # layer control to turn choropleth on or off
    folium.LayerControl().add_to(m)
    m.save(os.path.join('data & map', 'MahdiA3Q1_map({}).html'.format(legend_name.lower())))


def Coronavirus_Pie_Chart(case, countries):
    """ This Function Creates Pie Chart for data of the coronavirus"""
    now = datetime.datetime.now()
    plt.figure(figsize=(5, 5))
    plt.pie(case, labels=countries, autopct='%.1f%%')
    plt.title('Coronavirus Pie Chart on:  {}'.format(now.strftime('%c')))
    plt.savefig(os.path.join('data & map', 'MahdiA3Q1_Coronavirus Pie Chart.png'),transparent=True,bbox_inches='tight')


""" ***Getting coronavirus data from the internet and save them into a CSV file*** """

# getting the html format of the website
source = requests.get('https://www.worldometers.info/coronavirus/#countries').text
soup = BeautifulSoup(source, 'lxml')

# open a csv file and set its columns
csv_file = open(os.path.join('data & map','MahdiA3Q1_COVID-19 Live Data.csv'), 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Country', 'Total Cases', 'New Cases', 'Total Death', 'New Death', 'Total Recovered', 'Active Cases'])

# set the country counter to get exactly 200 countries
country_counter = 0
table = soup.find('table')

# go through all tr parts of the html
for tr in table.find_all('tr'):
    # set the counter to go through the statistics of each country
    counter = 0
    # go through all td parts of the html
    for td in tr.find_all('td'):
        # Find the country
        if td.find('a') is not None:
            country = td.find('a').text
            counter += 1
            country_counter += 1
        # go through the next td to get Total case
        elif counter == 1:
            Total_case = td.text.replace(',', '') if ',' in td.text else td.text
            counter += 1
        # go through the next td to get New case
        elif counter == 2:
            New_case = td.text.replace(',', '') if ',' in td.text else td.text
            if not New_case:
                New_case = '0'
            if New_case[0] == '+':
                New_case = New_case[1:]
            counter += 1
        # go through the next td to get Total Death
        elif counter == 3:
            Total_Death = td.text.replace(',', '') if ',' in td.text else td.text
            if Total_Death[-1] == ' ':
                Total_Death = Total_Death[:-1]
            if not Total_Death:
                Total_Death = '0'
            counter += 1
        # go through the next td to get New Death
        elif counter == 4:
            New_Death = td.text.replace(',', '') if ',' in td.text else td.text
            if not New_Death:
                New_Death = '0'
            if New_Death[0] == '+':
                New_Death = New_Death[1:]
            counter += 1
        # go through the next td to get Total Recovered
        elif counter == 5:
            Total_recovered = td.text.replace(',', '') if ',' in td.text else td.text
            if not Total_recovered:
                Total_recovered = '0'
            counter += 1
        # go through the next td to get Active cases
        elif counter == 6:
            Active_case = td.text.replace(',', '') if ',' in td.text else td.text
            if not Active_case:
                Active_case = '0'
            counter += 1

    # add all data to the csv file in row
    try:
        csv_writer.writerow([country, Total_case, New_case, Total_Death,New_Death, Total_recovered, Active_case])
    except:
        pass

# close the csv
csv_file.close()


""" ***Creating Choropleth maps for new cases, total cases, total death and total recovered*** """

# Getting data of Coronavirus and Territories of the countries
coronavirus = os.path.join('data & map', 'MahdiA3Q1_COVID-19 Live Data.csv')
countries = os.path.join('data & map', 'MahdiA3Q1_Countries.json')

# Read the csv file of Coronavirus data
coronavirus_data = pd.read_csv(coronavirus, encoding="ISO-8859-1")
# Read the Territories of the countries data
with open(countries) as f:
    geojson_counties = json.load(f)


# create a Choropleth map for new cases
Coronavirus_Choropleth_map(geojson_counties, 'choropleth',coronavirus_data, 'New Cases', 'YlOrRd')
# create a Choropleth map for total cases
Coronavirus_Choropleth_map(geojson_counties, 'choropleth',coronavirus_data, 'Total Cases', 'Purples')
# create a Choropleth map for total death
Coronavirus_Choropleth_map(geojson_counties, 'choropleth',coronavirus_data, 'Total Death', 'YlGn')
# create a Choropleth map for total recovered
Coronavirus_Choropleth_map(geojson_counties, 'choropleth',coronavirus_data, 'Total Recovered', 'RdPu')


""" ***Creating a pie chart for top 8 countries plus others*** """

# defining some variables
total_cases = []
total_countries = []
other_countries_cases = 0
counter2 = 0

# opening the corona data csv file.
with open(os.path.join('data & map', 'MahdiA3Q1_COVID-19 Live Data.csv'), 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # ignoring the column's names
    next(csv_reader)
    # adding all total cases and countries to 2 lists.
    for line in csv_reader:
        if counter2 == 211:
            break
        total_cases.append(line[1])
        total_countries.append(line[0])
        counter2 += 1

# get the first total cases of the first 8 countries.
diagram_cases = [int(i) for i in total_cases[:8]]
diagram_countries = total_countries[:8]
# add the other total cases of other countries to a new list.
for i in [int(case) for case in total_cases[8:]]:
    other_countries_cases += i

# add the "others" title to the Chart with stands for the rest of he countries total cases.
diagram_countries.append('Others')
# put the value of the other countries to the "others" title
diagram_cases.append(other_countries_cases)

# creating the pie chart and save it into the "data & map" directory
Coronavirus_Pie_Chart(diagram_cases, diagram_countries)

print("#########################################################################################")
print('Go To Data "data & map" directory to check the LIVE Diagram, Maps and data of Coronavirus')
print("The json file is for countries' boundaries and code uses this file.")
print("#########################################################################################")
