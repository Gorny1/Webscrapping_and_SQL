from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

# Program nie został stworzony w celach komercyjnych

# This is a webscraping app that uses bs4 and sqlite3.
# Scraped data contains flats, their locations, prices and link to the article from olx.pl
# Every information is displayed in console
# Then data is contained within SQL database


db = sqlite3.connect('dane.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE offers(Nazwa TEXT, Cena REAL, Dzielnica TEXT, Link TEXT) ''')
    quit()


def pricer(findprice):

    return float(findprice.replace(' ', '').replace('zł', '').replace(',', '.'))


def szukaj():

    for i in range(10):
        i = i+1
        path2 = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/poznan/?page={i}"
        page = get(path2)
        bs = BeautifulSoup(page.content, 'html.parser')

        for offer in bs.find_all('div', class_='offer-wrapper'):
            link = offer.find('a')
            link = link['href']
            footer = offer.find('td', class_='bottom-cell')
            loc = footer.find('small', class_="breadcrumb").get_text().strip().split(',')[0]
            loc = str(loc)
            title = offer.find('strong').get_text().strip()
            findPrice = pricer(offer.find('p', class_='price').get_text().strip())
            cursor.execute('INSERT INTO offers VALUES(?, ?, ?,?)', (title, findPrice, loc, link))
            db.commit()
            print(loc, title, findPrice)
            print(link)

    db.close()


szukaj()
