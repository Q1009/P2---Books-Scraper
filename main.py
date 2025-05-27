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

def get_article_data(incomplete_link : str = 'https://books.toscrape.com/'):
    complete_link = url + incomplete_link
    response = requests.get(complete_link)

    if response.status_code == 200:
        data_to_store = {}
        article_soup = BeautifulSoup(response.text, "html.parser")
        data_to_store["title"] = article_soup.find("article").find("h1").text
        rating = article_soup.find("article").find("div", {"class" : "col-sm-6 product_main"}).find_all("p")
        rating2 = rating[2]
        rating3 = rating2["class"]
        rating4 = rating3[1]
        data_to_store["rating"] = rating4
        #description = article_soup.find("article").find_all("p")
        #print(description[3].text)
        trs = article_soup.find_all("tr")
        for tr in trs:
            for (th, td) in zip(tr.find_all("th"), tr.find_all("td")):
                data_to_store[th.text.lower()] = td.text
        #Getting rid of the pound symbol
        data_to_store["price (excl. tax)"] = data_to_store["price (excl. tax)"][slice(2,-1,1)]
        data_to_store["price (incl. tax)"] = data_to_store["price (incl. tax)"][slice(2,-1,1)]
        data_to_store["tax"] = data_to_store["tax"][slice(2,-1,1)]
        
        #Adding the dictionary to the list
        article_data.append(data_to_store)
        
        

link = get_article_link(url)
print("Hello World !")
article_data = []
get_article_data(link)
print(article_data)

# def scrape_book():
"""
This function scrapes the html code and return a dictionary of all the elements of the product
"""

# récupérer avec une fonction les infos d'un livre
# récupérer avec une fonction tous les livres d'une catégorie