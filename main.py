import requests
from bs4 import BeautifulSoup
import csv
import os

# Instance of object type str as the url of the website
url : str = 'https://books.toscrape.com/'

def extract_category_data(url : str) -> list : #Etre précis dans le typage, liste de quoi ?
    # Intance of object type list to hold all links
    extracted_category_data : list[dict[str, str]] = []
    # Instance of object type requests
    r = requests.get(url)
    # Verification of network establishment
    if r.status_code == 200:
        # Instance of object type BeautifulSoup
        soup : BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        # Getting every category name and url on the website
        for li in soup.find('ul', class_ = 'nav nav-list').find('li').find('ul').find_all('li'):
            extracted_data = {}
            extracted_data['category_name'] = li.find('a').string.strip()
            extracted_data['category_url'] = url + li.find('a')['href']
            # Adding the dictionnary to the list
            extracted_category_data.append(extracted_data)

    return extracted_category_data

def create_directories_and_urls_file(extracted_category_data):
    parent_directory_name = 'Books'
    try:
        os.mkdir(parent_directory_name)
        print(f"Directory '{parent_directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{parent_directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{parent_directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    with open('Books/category_urls_output.txt', 'w') as file_txt:
        for category_data in extracted_category_data:
            file_txt.write(category_data['category_url'] + '\n')
            nested_directory = parent_directory_name + '/' + category_data['category_name']
            try:
                os.mkdir(nested_directory)
                print(f"Nested directories '{nested_directory}' created successfully.")
            except FileExistsError:
                print(f"One or more directories in '{nested_directory}' already exist.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{nested_directory}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
        



def extract_article_links(url : str) -> list[str] : #Etre précis dans le typage, liste de quoi ?
    # Intance of object type list to hold all links
    article_links : list = []
    response = requests.get(url)

    if response.status_code == 200:
        # Instance of object type BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        if not soup.find('ul', class_ = 'pager'):
            # Getting every article url in the page
            for li in soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'):
                link = li.find('h3').find('a')['href'][9:]
                article_links.append(link)

        else:
            # Getting rid of index.html and replacing it by page-i.html
            i = 1
            url_category_page : str = url[:-10] + 'page-' + str(i) + '.html'
            # Instance of object type requests.models.Response
            r = requests.get(url_category_page)

            while r.status_code != 404:
                # Verification of network establishment
                if r.status_code == 200:
                    # Instance of object type BeautifulSoup
                    soup : BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
                    # Getting every article url in the page
                    for li in soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'):
                        link = li.find('h3').find('a')['href'][9:]
                        article_links.append(link)

                    # Go to next page    
                    i += 1
                    url_category_page = url[:-10] + 'page-' + str(i) + '.html'
                    r = requests.get(url_category_page)

    return article_links
            


def get_article_data(name_of_category : str =''): # incomplete_link : str = 'https://books.toscrape.com/'
    extracted_article_data = []
    with open ('Books/' + name_of_category + '/' + name_of_category + '_book_urls.txt', 'r') as file_txt:
        for row in file_txt:
            response = requests.get(row.strip()) # Le goulot est là (en termes de rapidité d'exécution)

            if response.status_code == 200:
                extracted_data = {}
                extracted_data['product_page_url'] = row.strip()
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
     
def load_article_data(data_to_load, name_of_category):
    # data to load is a list of dictionaries
    with open('Books/' + name_of_category + '/' + name_of_category + '_book_data.csv', 'w', newline='') as file_csv:
        header = (data_to_load[0].keys())
        writer = csv.DictWriter(file_csv, fieldnames=header)
        writer.writeheader()
        number_of_books = 0
        for row in data_to_load:
            writer.writerow(row)
            number_of_books += 1
        print(f'{number_of_books} books loaded.')

    return number_of_books

def load_article_urls(urls_to_load : list[str] = [], name_of_category : str = 'Asupp'):
    with open('Books/' + name_of_category + '/' + name_of_category + '_book_urls.txt', 'w') as file_txt:
        for row in urls_to_load:
            file_txt.write(url + 'catalogue/' + row + '\n')


# Main

category_data_to_load = extract_category_data(url)
create_directories_and_urls_file(category_data_to_load)
category_number = 1
book_number = 0

for category_data in category_data_to_load:
    print(f'In category n°{category_number} :')
    article_urls_to_load = extract_article_links(category_data['category_url'])
    load_article_urls(article_urls_to_load, category_data['category_name'])
    article_data_to_transform = get_article_data(category_data['category_name'])
    article_data_to_load = transform_article_data(article_data_to_transform)
    books_loaded = load_article_data(article_data_to_load, category_data['category_name'])
    book_number = book_number + books_loaded
    category_number += 1

print(f'Script finished with {book_number} books loaded.')
