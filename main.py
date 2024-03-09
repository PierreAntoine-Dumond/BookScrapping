import requests 

url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    print(html)
else:
    print('ERREUR', response.status_code)

print('FIN')