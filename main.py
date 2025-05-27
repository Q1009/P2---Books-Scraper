import requests
from bs4 import BeautifulSoup
import csv

# Instance of object type str as the url of the website
url : str = 'https://books.toscrape.com/'


def get_article_link(url : str = 'https://books.toscrape.com/') -> str :
    # Instance of object type requests.models.Response
    r : requests.models.Response = requests.get(url)

    # Verification of network establishment
    if r.status_code == 200:
        # Instance of object type BeautifulSoup
        soup : BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        balise_section = soup.find('section')
        balise_li = balise_section.find('li')
        balise_h3 = balise_li.find('h3')
        balise_a = balise_h3.find('a')
        lien = balise_a['href']

    return lien



def get_article_data(incomplete_link : str = 'https://books.toscrape.com/'):
    complete_link = url + incomplete_link
    response = requests.get(complete_link)

    if response.status_code == 200:
        extracted_article_data = []
        extracted_data = {}
        extracted_data['product_page_url'] = complete_link
        article_soup = BeautifulSoup(response.text, 'html.parser')
        extracted_data['title'] = article_soup.find('article').find('h1').text
        rating = article_soup.find('article').find('div', {'class' : 'col-sm-6 product_main'}).find_all('p')
        rating2 = rating[2]
        rating3 = rating2['class']
        rating4 = rating3[1]
        extracted_data['review_rating'] = rating4
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
    transformed_data = {}
    for data in data_to_transform:
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

        
def load_article_data(data_to_load):
    with open('output.csv', 'w', newline='') as file_csv:
        header = (data_to_load[0].keys())
        writer = csv.DictWriter(file_csv, fieldnames=header)
        writer.writeheader()
        for row in data_to_load:
            writer.writerow(row)
            


link = get_article_link(url)
#article_data = []
#get_article_data(link)
#print(article_data)
article_data_to_transform = get_article_data(link)
article_data_to_load = transform_article_data(article_data_to_transform)
load_article_data(article_data_to_load)

print("data loaded")

# def scrape_book():
"""
This function scrapes the html code and return a dictionary of all the elements of the product
"""

# récupérer avec une fonction les infos d'un livre
# récupérer avec une fonction tous les livres d'une catégorie