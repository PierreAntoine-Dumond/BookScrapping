import requests
import csv
from bs4 import BeautifulSoup


def get_text_is_not_none(e):
    if e:
        return e.text.strip()
    return None

# Fonction non fonctionnelle
def extract(file):

    data = {"product_page_url": "", "universal_product_code": "", "price_including_tax": "", "price_excluding_tax": "",
            "number_available": "", "product_description": "", "category": "", "review_rating": "", "image_url": ""}

    bs = BeautifulSoup(file, "html5lib")
    data["title"] = bs.find("h3").text
    return data

# Envoi d'une requête au fichier à scrapper / Création d'un fichier html / Parsage
def write_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # Ecriture de la requête html dans un nouveau fichier
        with open("booktoscrape", "w") as f:
            f.write(html)

        soup = BeautifulSoup(html, 'html5lib')
        # titre = get_text_is_not_none(soup.find("div", class_="product_price"))
        # print(titre)

        # Récupération des titres h3
        e_titre = soup.find_all('h3')
        for title in e_titre:
            print(title.text)
    else:
        print('ERREUR', response.status_code)

# Parsage dans un fichier existant
def read_file(file: str):
    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
        f_content = f.read()

    soup = BeautifulSoup(f_content, 'html5lib')
    print('## -- Extraction des données... -- ##')
    '''
    Éxtraction des données & Écriture dans un fichier csv

    data_title_to_append = []
    l_titre = soup.find_all('h3')
    for title in l_titre:
        data_title_to_append.append(title.text)

    for data in data_title_to_append:
        print(data)
    '''

    data_cate_to_append = []
    side_cate = soup.find("div", class_="side_categories")
    if side_cate is not None:
        l_categorie = side_cate.find_all('a')
        for cate in l_categorie:
            # print(cate.text)
            data_cate_to_append.append(cate.text.strip())
    else:
        print(side_cate)
        print('None')

    for data in data_cate_to_append:
        print(data)
    
    # with csv.open_csv('data.csv') as reader:  # doctest: +SKIP
    #     for row in reader:
    #         print(', '.join(row))

# write_file('https://books.toscrape.com/')
        #https://books.toscrape.com/catalogue/page-2.html
read_file('booktoscrape')
print('FIN')
