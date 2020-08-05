import sqlite3

from bs4 import BeautifulSoup
import pandas as pd
import requests
from openpyxl.workbook import Workbook
import sqlite3


#declaring first variables and url
price2 = []
titel2 = []
input= 'guitarra-acustica-gibson'
url= 'https://listado.mercadolibre.com.ar/'

#first scrap to collect data
page = requests.get(url+input)
soup = BeautifulSoup(page.content, 'html.parser')
tuples = []

for result in soup.find_all('div', class_='item__info'):
    price = result.find('span', class_='price__fraction').get_text()
    price = str(price)
    price = price.replace(".", "")
    price = price.replace(",", ".")
    title = result.find('span', class_='main-title').get_text()
    try:
        cuotas = result.find('span', class_='item-installments-text').get_text()
    except:
        cuotas = 0
    try:
        envio = result.find('span', class_='text-shipping').get_text()
    except:
        envio = 0
    tuple = (int(price), str(title), str(cuotas), str(envio))
    tuples.append(tuple)
print(len(tuples))

#function to get next page link
def getlink2(soup):
    button = soup.find('a', class_='andes-pagination__link prefetch')
    return button

print(getlink2(soup).get('href'))

#getting url to initiate the while loop
url2 = getlink2(soup).get('href')
page2 = requests.get(url2)
soup2 = BeautifulSoup(page2.content, 'html.parser')


#while loop to collect data from all the results pages including the last one with the else statement
while getlink2(soup2):
    for result in soup2.find_all('div', class_='item__info'):
        price = result.find('span', class_='price__fraction').get_text()
        price = str(price)
        price = price.replace(".", "")
        price = price.replace(",", ".")
        title = result.find('span', class_='main-title').get_text()
        try:
            cuotas = result.find('span', class_='item-installments-text').get_text()
        except:
            cuotas = 0
        try:
            envio = result.find('span', class_='text-shipping').get_text()
        except:
            envio = 0
        tuple = (int(price), str(title), str(cuotas), str(envio))
        tuples.append(tuple)
    url2 = getlink2(soup2)
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')

else:
    for result in soup2.find_all('div', class_='item__info'):
        price = result.find('span', class_='price__fraction').get_text()
        price = str(price)
        price = price.replace(".", "")
        price = price.replace(",", ".")
        title = result.find('span', class_='main-title').get_text()
        try:
            cuotas = result.find('span', class_='item-installments-text').get_text()
        except:
            cuotas = 0
        try:
            envio = result.find('span', class_='text-shipping').get_text()
        except:
            envio = 0
        tuple = (int(price), str(title), str(cuotas), str(envio))
        tuples.append(tuple)


#creating dataframe to dump data and write to xlsx for further use
df = pd.DataFrame(tuples, columns=['price','title','cuotas','envio'])
df.to_excel('data.xlsx')
print(df.describe())

#creating a SQL database for further use
connection = sqlite3.connect("data.db")
crsr = connection.cursor()
sql_command = """create table results (
key INTEGER PRIMARY KEY AUTOINCREMENT,
price Real,
description VARCHAR(500),
cuotas VARCHAR(30),
envio VARCHAR(30));"""
crsr.execute(sql_command)
crsr.executemany("insert into results (price, description, cuotas, envio) values (?, ?, ?, ?)", tuples)
connection.commit()
crsr.execute("SELECT * FROM results")
ans = crsr.fetchmany(6)
print(ans)


