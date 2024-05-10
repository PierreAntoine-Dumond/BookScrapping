import requests
from bs4 import BeautifulSoup
import main
import time


def recup_all_categorie(url):

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text

        with open("booktoscrape", "w", encoding='utf-8') as f:
            f.write(html)

        soup = BeautifulSoup(html, 'html5lib')

        print('Liste catéogrie trouver dans booktoscrape :')
        l_url = []
        start_url_to_add = 'https://books.toscrape.com/'
        side = soup.find('ul', class_='nav nav-list')
        print(side.text)
        all_a = side.find_all('a', href=True)
        for a in all_a[1::]:
            url_a = a.get('href')
            add_http_url_a = start_url_to_add + url_a
            print(add_http_url_a)
            l_url.append(url_a)
    else:
        print('ERREUR code status')
    return l_url


# Cette fonction regarde si une page suivante est existante à la catégorie. 
def try_to_find_pages(urls):

    print('JE CHERCHE LE NOMBRE DE PAGE A SCRAPPER DANS CETTE CATÉGORIE !')
    
    i = 1
    for url in urls:
        for i in range(50):
            i += 1
            url = url.replace('index.html', f'page{i}')
            print(url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    urls.insert(url)
            except:
                print("Erreur status code")
    return urls
