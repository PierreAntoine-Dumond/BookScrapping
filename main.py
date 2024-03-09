import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    # print(html)
    f = open("booktoscrape", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, 'html5lib')
    soup.find()
else:
    print('ERREUR', response.status_code)

print('FIN')
