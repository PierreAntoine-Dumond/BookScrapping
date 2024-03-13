import csv
import requests
import time
from bs4 import BeautifulSoup

## -- Ce scrypt sert à récupérer toutes les données d'une page produit -- ##
## --                            ET                                    -- ##
## -- A créer, ajouter ou transformer les données dans un fichier csv  -- ##


def get_text_is_not_none(e):
    if e:
        return e.text.strip()
    return None

data = {"product_page_url": [], "universal_product_code": [], "title": [], "price_including_tax": [], "price_excluding_tax": [],
            "number_available": [], "product_description": [], "category": [], "review_rating": [], "image_url": []}

# Cette fonction écrit ou réecrit à l'intérieur du fichier <booktoscrape> -> Le crée si inexistant dans le dossier courant
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

# Cette fonction lit le fichier -> elle est conçue pour extraire toutes les informations de la fiche produit
def read_file(file: str, url):

    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r", encoding='utf-8') as f:
        f_content = f.read()
    print()
    soup = BeautifulSoup(f_content, 'html5lib')
    print('## -- Extraction des données... -- ##')
    print()

    #Éxtraction des données depuis l'html -> Ajout des éléments à l'intérieur du dictionnaire
    data['product_page_url'].append(url)


    print("EXTRACTION HTML TABLE...")
    extract_table_data = []
    table = soup.find('table', class_="table table-striped")
    if table:
        td = table.find_all('td')
        for d in td:
            extract_table_data.append(d.text.strip())
        print("Les données sont insérés dans le dictionnaire data.")
    else:
        print("Aucun élément <table> trouvé avec la class 'table table-striped'")
    data['universal_product_code'].append(extract_table_data[0])
    data['price_excluding_tax'].append(extract_table_data[2])
    data['price_including_tax'].append(extract_table_data[3])
    data['number_available'].append(extract_table_data[5])
    data['review_rating'].append(extract_table_data[6])
    print()


    print('EXTRACTION TITLE...')
    titre = get_text_is_not_none(soup.find('h1'))
    print("Le titre est : ", titre)
    data['title'].append(titre)
    print()


    print("EXTRACTION DESCRIPTION...")
    # Ici, lors de la mise en place du code j'ai utilisé une variable i que j'ai indenté pour savoir ou se situaait la bonne description.
    data_p = []
    descritpion = soup.find_all("p")
    if descritpion:
        for p in descritpion:
            data_p.append(p.text)
        print("La description est : ", data_p[3])
        data['product_description'].append(data_p[3])
    else:
        print("Aucun élément <p> trouvé")
    print()


    print("EXTRACTION CATEGORY...")
    # Ici, lors de la mise en place du code j'ai utilisé une variable i que j'ai indenté pour savoir ou se situaait la bonne catégorie.
    # Il faut l'utiliser qu'une fois après avoir chargé l'intégralité des urls des fiches produits
    data_cate = []
    category_data_ul = soup.find('ul')
    if category_data_ul:
        category_a = category_data_ul.find_all('a')
        for cate in category_a:
            data_cate.append(cate.text)
        print("La catégorie est : ", data_cate[2])
        data['category'].append(data_cate[2])
    else:
        print("Aucun élément <ul> trouvé")
    print()


    print("EXTRACTION IMAGE")
    img_element = soup.find('div', id='product_gallery').find('img')
    # Vérifier si l'élément img a été trouvé
    if img_element:
        # Extraire l'URL de l'image
        image_url = img_element['src']
        char_to_remove = "../.."
        image_url = image_url.replace(char_to_remove, 'https://books.toscrape.com')
        print("URL de l'image :", image_url)
    else:
        print("Aucun élément <img> trouvé avec l'ID 'product_gallery'\n")
    data['image_url'].append(image_url)


    print("RESULTAT EXTRACTION :\n")
    print(data)

    return data

# Cette fonction récupère les urls à l'intérieur d'une catégorie et remplace les caractères pour obtenir un lien opérationnel.
def extract_url(file, urls):

    path_url_to_extract = 'https://books.toscrape.com/catalogue/'
    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
        f_content = f.read()
    soup = BeautifulSoup(f_content, "html5lib")

    scrap_url_ol = soup.find("ol", class_='row')
    scrap_url_href = scrap_url_ol.find_all('a', href=True)
    for url in scrap_url_href[::2]:
        url = url.get('href')
        print(url)
        url = url.replace('../../..', path_url_to_extract)
        print(url)
        urls.append(url)
    print(urls)

    return

# Cette fonction regarde si une page suivante est existante à la catégorie. 
def try_to_find_pages(file, url_present_page, l_url_page):

    print('JE CHERCHE LE NOMBRE DE PAGE A SCRAPPER DANS CETTE CATÉGORIE !')
    first_time = True
    next_page = True
    i = 1
    i2 = 2
    while next_page:
        with open(file, "r") as f:
            f_content = f.read()
        soup = BeautifulSoup(f_content, "html5lib")
        try:
            print("Une seconde, je vérifie si une page suivante est existante dans cette catégorie...")
            scrap_url_pager = soup.find("li", class_='next')
            if scrap_url_pager and first_time == True:
                print('On dirait qu\'une seconde page eut été découverte.')
                time.sleep(1)
                scrap_url_next_href = scrap_url_pager.find('a', href=True)
                url_scrap_next = scrap_url_next_href.get('href')
                url_next = url_present_page.replace('index.html', url_scrap_next)
                print(url_next)
                l_url_page.append(url_next)
                write_file(url_next)
                url_scrap_last = url_scrap_next
                print("Je suis l'url scrap_last : ",url_scrap_last)
            elif scrap_url_pager:
                first_time = False
                scrap_url_next_href = scrap_url_pager.find('a', href=True)
                url_scrap_next = scrap_url_next_href.get('href')
                print("On dirait qu'il existe plusieurs pages. Laisse moi récupérer ses urls !")
                time.sleep(1)
                print(url_present_page)
                url_next = url_present_page.replace(url_scrap_last, url_scrap_next)
                print(url_next)
                l_url_page.append(url_next)
                write_file(url_next)
                url_scrap_last = url_next
            else:
                print('J\'ai terminé d\'avaler les urls ! Plus aucune page dans cette catégorie.. C\'était.. Délicieux !')
                del l_url_page[-1]
                next_page = False
        except:
            print("Intéréssant, je n'ai pas trouvé de balise <a href> dans cette catégorie..")

    return l_url_page.append(url_next)
    

def create_add_or_transform_data_in_csv_file(data):
    # Edition et transformation des données dans un fichier csv
    print("Transformation des données dans un fichier CSV...")

    # Récupérer les clés du dictionnaire
    keys = data.keys()

    # Transposer les listes pour obtenir les données par produit
    product_data = zip(*[data[key] for key in keys])
    print(product_data)
    with open('data_book.csv', 'w', newline='', encoding='utf-8') as file:
        # Créer un objet DictWriter avec les clés du dictionnaire
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()

        # Écrire les données de chaque produit dans le fichier CSV
        for product in product_data:
            writer.writerow(dict(zip(keys, product)))

urls = []
url_page = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']
write_file(url_page[0])
try_to_find_pages('booktoscrape',url_page[0], url_page)
for u in url_page:
    print('Page suivante : ', u)
    write_file(u)
    extract_url('booktoscrape', urls)

for url in urls:
    print('Scrapping des données en cours... ' + url)
    write_file(url)
    read_file('booktoscrape', url)
    print(data)
create_add_or_transform_data_in_csv_file(data)
print('FIN')
