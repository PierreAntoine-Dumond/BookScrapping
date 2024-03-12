import requests
from bs4 import BeautifulSoup


# Envoi d'une requête au fichier à scrapper / Création d'un fichier html / Parsage
def write_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # Ecriture de la requête html dans un nouveau fichier
        with open("booktoscrape", "w", encoding='utf-8') as f:
            f.write(html)

        soup = BeautifulSoup(html, 'html5lib')
        # titre = get_text_is_not_none(soup.find("div", class_="product_price"))
        # print(titre)

        # Récupération des titres h3
        print("Titre trouvé dans le nouvel URL : \n")
        e_titre = soup.find_all('h3')
        for title in e_titre:
            print(title.text)
        print()
    else:
        print('ERREUR', response.status_code)


# write_file('https://books.toscrape.com/catalogue/see-america-a-celebration-of-our-national-parks-treasured-sites_732/')
# read_file('booktoscrape')
print('FIN')