from bs4 import BeautifulSoup
from main import write_file


def extract_url(file):

    urls = []
    print('## -- Lecture du fichier en cours... -- ##')
    with open(file, "r") as f:
        f_content = f.read()
    soup = BeautifulSoup(f_content, "html5lib")

    scrap_url_ol = soup.find("ol", class_='row')
    scrap_url_href = scrap_url_ol.find_all('a', href=True)
    for url in scrap_url_href[::2]:
        url = url.get('href')
        url = url.replace('../../..', 'https://books.toscrape.com/catalogue')
        urls.append(url)
    print(urls)


write_file('https://books.toscrape.com/catalogue/category/books/travel_2/index.html')
extract_url('booktoscrape')