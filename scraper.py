from bs4 import BeautifulSoup
import pandas as pd
import requests
from openpyxl.workbook import Workbook

#declaring first variables and url
price2 = []
titel2 = []
input= 'guitarra-acustica'
url= 'https://listado.mercadolibre.com.ar/'

#first scrap to collect data
page = requests.get(url+input)
soup = BeautifulSoup(page.content, 'html.parser')
price = soup.find_all('span', class_='price__fraction')
title = soup.find_all('span', class_='main-title')
price2 = [p2.get_text() for p2 in price]
title2 = [t2.get_text() for t2 in title]
print(len(price2))

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
while getlink2(soup2) :
    pricen = soup2.find_all('span', class_='price__fraction')
    titlen = soup2.find_all('span', class_='main-title')
    price2.extend(p2n.get_text() for p2n in pricen)
    title2.extend(t2n.get_text() for t2n in titlen)
    url2 = getlink2(soup2).get('href')
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
else:
    pricen = soup2.find_all('span', class_='price__fraction')
    titlen = soup2.find_all('span', class_='main-title')
    price2.extend(p2n.get_text() for p2n in pricen)
    title2.extend(t2n.get_text() for t2n in titlen)

#creating dataframe to dump data and write to xlsx for further use
df = pd.DataFrame(title2 , price2)
df.to_excel('data.xlsx')
print(df.describe)



####################################

