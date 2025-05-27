import requests
from bs4 import BeautifulSoup

# Instance of object type str as the url of the website
url : str = 'https://books.toscrape.com/'

def get_article_link(url : str = 'https://books.toscrape.com/') -> str :
    # Instance of object type requests.models.Response
    r : requests.models.Response = requests.get(url)

    # Verification of network establishment
    if r.status_code == 200:
        # Instance of object type BeautifulSoup
        soup : BeautifulSoup = BeautifulSoup(r.text, "html.parser")
        balise_section = soup.find("section")
        balise_li = balise_section.find("li")
        balise_h3 = balise_li.find("h3")
        balise_a = balise_h3.find("a")
        lien = balise_a['href']

    return lien


link = get_article_link(url)
print("Hello World !")
print(link)

# def scrape_book():
"""
This function scrapes the html code and return a dictionary of all the elements of the product
"""

# récupérer avec une fonction les infos d'un livre
# récupérer avec une fonction tous les livres d'une catégorie