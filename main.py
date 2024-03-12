import requests
import csv
from bs4 import BeautifulSoup


def get_text_is_not_none(e):
    if e:
        return e.text.strip()
    return None


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

# Parsage dans un fichier existant
def read_file(file: str):

    data = {"product_page_url": [], "universal_product_code": [], "title": [], "price_including_tax": [], "price_excluding_tax": [],
            "number_available": [], "product_description": [], "category": [], "review_rating": [], "image_url": []}

    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
        f_content = f.read()

    soup = BeautifulSoup(f_content, 'html5lib')
    print('## -- Extraction des données... -- ##')

    #Éxtraction des données à l'intérieur du dico à l'emplacement

    l_titre = soup.find_all('h3')
    for t in l_titre:
        data['title'].append(t.text.strip())

    print('TITLE')
    for d in data['title']:
        print(d)
    print()

    side_cate = soup.find("div", class_="side_categories")
    if side_cate is not None:
        l_categorie = side_cate.find_all('a')
        for cate in l_categorie:
            data['category'].append(cate.text.strip())
    else:
        print(side_cate)
        print('None')

    print('CATEGORY')
    for d in data['category']:
        print(d)
    print()

    with open('data.csv', 'w') as csvfile:
        dico_data = ["product_page_url","universal_product_code","title","price_including_tax","price_excluding_tax",
            "number_available","product_description","category","review_rating","image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=dico_data)
        writer.writeheader()
        writer.writerow({"product_page_url":"","universal_product_code":"","title":'A Light in the ...',"price_including_tax":'',"price_excluding_tax":'',
            "number_available":'',"product_description":'',"category":'Books',"review_rating":'',"image_url":''})


# write_file('https://books.toscrape.com/')
        #https://books.toscrape.com/catalogue/page-2.html
write_file('https://books.toscrape.com/catalogue/see-america-a-celebration-of-our-national-parks-treasured-sites_732/')
# read_file('booktoscrape')
print('FIN')