import csv
from bs4 import BeautifulSoup


def read_file(file: str):

    data = {"product_page_url": [], "universal_product_code": [], "title": [], "price_including_tax": [], "price_excluding_tax": [],
            "number_available": [], "product_description": [], "category": [], "review_rating": [], "image_url": []}

    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
        f_content = f.read()
    print()
    soup = BeautifulSoup(f_content, 'html5lib')
    print('## -- Extraction des données... -- ##')
    print()

    #Éxtraction des données depuis l'html -> Ajout des éléments à l'intérieur du dictionnaire
    data['product_page_url'].append('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')


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
        print("URL de l'image :", image_url)
    else:
        print("Aucun élément <img> trouvé avec l'ID 'product_gallery'\n")
    data['image_url'].append(image_url)


    print("RESULTAT EXTRACTION :\n")
    print(data)

    # Edition et transformation des données dans un fichier csv
    print("Transformation des données dans un fichier CSV...")
    with open('data_book.csv', 'w') as file:
        dico_data = ["product_page_url","universal_product_code","title","price_including_tax","price_excluding_tax",
            "number_available","product_description","category","review_rating","image_url"]
        writer = csv.DictWriter(file, fieldnames=dico_data)
        writer.writeheader()
        writer.writerow(data)

read_file('booktoscrape')
