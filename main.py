import requests
from bs4 import BeautifulSoup
import csv
import os

# Instance of object type str as the url of the website
url : str = 'https://books.toscrape.com/'
url_fantasy : str = 'https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'

def extract_article_links(url : str) -> list : #Etre précis dans le typage, liste de quoi ?
    # Intance of object type list to hold all links
    links : list = []
    # Getting rid of index.html and replacing it by page-i.html
    i = 1
    url_category_page : str = url[:-10] + 'page-' + str(i) + '.html'
    # Instance of object type requests.models.Response
    r : requests.models.Response = requests.get(url_category_page)

    while r.status_code != 404:
        # Verification of network establishment
        if r.status_code == 200:
            # Instance of object type BeautifulSoup
            soup : BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
            # Getting every article url in the page
            for li in soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'):
                link = li.find('h3').find('a')['href'][9:]
                links.append(link)

            # Go to next page    
            i += 1
            url_category_page = url[:-10] + 'page-' + str(i) + '.html'
            r : requests.models.Response = requests.get(url_category_page)

    return links
            


def get_article_data(): # incomplete_link : str = 'https://books.toscrape.com/'
    extracted_article_data = []
    with open ('article_urls_output.txt', 'r') as file_txt:
        for row in file_txt:
            complete_link = url + row.strip()
            response = requests.get(complete_link) # Le goulot est là (en termes de rapidité d'exécution)

            if response.status_code == 200:
                extracted_data = {}
                extracted_data['product_page_url'] = complete_link
                article_soup = BeautifulSoup(response.text, 'html.parser') # passer en parametre une option d'encoding UTF 8
                extracted_data['title'] = article_soup.find('article').find('h1').text
                rating = article_soup.find('article').find('div', class_ = 'col-sm-6 product_main').find_all('p')
                rating2 = rating[2]
                rating3 = rating2['class']
                rating4 = rating3[1]
                extracted_data['review_rating'] = rating4 # convertir en chiffre () avec une table de conversion
                description = article_soup.find('article').find_all('p')
                extracted_data['product_description'] = description[3].text
                image_url = article_soup.find('article').find('img')
                extracted_data['image_url'] = url + image_url['src'][6:]
                category = article_soup.find('ul').find_all("li")
                extracted_data['category'] = category[2].find('a').text
                trs = article_soup.find_all('tr')
                for tr in trs:
                    for (th, td) in zip(tr.find_all('th'), tr.find_all('td')):
                        extracted_data[th.text.lower()] = td.text
                #Getting rid of the pound symbol
                extracted_data['price (excl. tax)'] = extracted_data['price (excl. tax)'][2:]
                extracted_data['price (incl. tax)'] = extracted_data['price (incl. tax)'][2:]
                extracted_data['tax'] = extracted_data['tax'][2:]
                
                #Adding the dictionary to the list
                extracted_article_data.append(extracted_data)

    return extracted_article_data

def transform_article_data(data_to_transform):
    transformed_article_data = []
    for data in data_to_transform:
        transformed_data = {}
        transformed_data['product_page_url'] = data['product_page_url']
        transformed_data['universal_product_code'] = data['upc']
        transformed_data['title'] = data['title']
        transformed_data['price_including_tax'] = data['price (incl. tax)']
        transformed_data['price_excluding_tax'] = data['price (excl. tax)']
        transformed_data['number_available'] = data['availability'] # le nombre n'est pas isolé
        transformed_data['product_description'] = data['product_description']
        transformed_data['category'] = data['category']
        transformed_data['review_rating'] = data['review_rating']
        transformed_data['image_url'] = data['image_url']

        #Adding the dictionary to the list
        transformed_article_data.append(transformed_data)


    return transformed_article_data
     
def load_article_data(data_to_load): # Mettre un nom de fichier par catégorie (os mkdir pour le répertoire)
    # data to load is a list of dictionaries
    with open('article_data_output.csv', 'w', newline='') as file_csv:
        header = (data_to_load[0].keys())
        writer = csv.DictWriter(file_csv, fieldnames=header)
        writer.writeheader()
        for row in data_to_load:
            writer.writerow(row)

def load_article_urls(urls_to_load : list = []):
    with open('article_urls_output.txt', 'w') as file_txt:
        for row in urls_to_load:
            file_txt.write('catalogue/' + row + '\n')


"""

Créer un dossier par catégorie -> on y retrouve le csv et toutes les images
#main

#article_urls_to_load = extract_article_links(url_fantasy)
#load_article_urls(article_urls_to_load)
article_data_to_transform = get_article_data()
article_data_to_load = transform_article_data(article_data_to_transform)
print(len(article_data_to_load))
#print(article_data_to_load[0])
#load_article_data(article_data_to_load)
print("data loaded")

"""

