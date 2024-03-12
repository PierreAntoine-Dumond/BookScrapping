import csv
from bs4 import BeautifulSoup
from main import write_file


urls = ['https://books.toscrape.com/catalogue/see-america-a-celebration-of-our-national-parks-treasured-sites_732/', 
       'https://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html']


def get_text_is_not_none(e):
    if e:
        return e.text.strip()
    return None

data = {"product_page_url": [], "universal_product_code": [], "title": [], "price_including_tax": [], "price_excluding_tax": [],
            "number_available": [], "product_description": [], "category": [], "review_rating": [], "image_url": []}

def read_file(file: str, url):

    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
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


# def create_add_or_transform_data_in_csv_file(data):
#     # Edition et transformation des données dans un fichier csv
#     print("Transformation des données dans un fichier CSV...")
#     with open('data_book.csv', 'w') as file:
#         dico_data = ["product_page_url","universal_product_code","title","price_including_tax","price_excluding_tax",
#             "number_available","product_description","category","review_rating","image_url"]
#         writer = csv.DictWriter(file, fieldnames=dico_data)
#         writer.writeheader()
#         for row in data:
#             if isinstance(row, dict):  # Vérification si la ligne est un dictionnaire
#                 writer.writerow(row)
#             else:
#                 print(f"Ignorer la ligne invalide : {row}")


def create_add_or_transform_data_in_csv_file(data):
    # Edition et transformation des données dans un fichier csv
    print("Transformation des données dans un fichier CSV...")

    # Récupérer les clés du dictionnaire
    keys = data.keys()

    # Transposer les listes pour obtenir les données par produit
    product_data = zip(*[data[key] for key in keys])
    print(product_data)
    '''
    with open('data_book.csv', 'w', newline='', encoding='utf-8') as file:
        # Créer un objet DictWriter avec les clés du dictionnaire
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()

        # Écrire les données de chaque produit dans le fichier CSV
        for product in product_data:
            writer.writerow(dict(zip(keys, product)))
    '''

for url in urls:
    write_file(url)
    read_file('booktoscrape', url)
print(data)
create_add_or_transform_data_in_csv_file(data)
