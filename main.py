import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import io
from PIL import Image

# Instance of object type str as the url of the website
url: str = 'https://books.toscrape.com/'


def extract_category_data(url: str) -> list[dict[str, str]]:
    """
    This function scraps the home page of the website in search
    of all the book categories available.
    Returns a list of dictionaries containing the category name
    and the category url.

        Parameters:
            url (str): the string of the website's url

        Returns:
            extracted_category_data (list[dict[str, str]]): the list
            of dictionaries containing the name and the url
            of a category as strings
            dict_keys(['category_name', 'category_url'])
    """
    # Instance of object type list to hold all dictionaries
    extracted_category_data: list[dict[str, str]] = []
    # Instance of object type requests
    response = requests.get(url)
    # Verification of website connection
    if response.status_code == 200:
        # Instance of object type BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Getting every category name and url on the website
        for li in soup.find('ul', class_='nav nav-list').find(
                'li').find('ul').find_all('li'):
            extracted_data: dict[str, str] = {}
            extracted_data['category_name'] = li.find(
                'a').string.strip()
            extracted_data['category_url'] = url + li.find(
                'a')['href']
            # Adding the dictionary to the list
            extracted_category_data.append(extracted_data)
            # Should I delete the temporary dictionary here ?

    return extracted_category_data


def create_directories_and_urls_file(extracted_category_data:
                                     list[dict[str, str]]) -> None:
    """
    This function creates a local parent directory named 'Books'
    and then a child directory per category.
    In the parent directory, creates a .txt file containing every
    category url.

        Parameters:
            extracted_category_data (list[dict[str, str]]): the list
            of dictionaries containing the name and the url of a
            category as strings
            dict_keys(['category_name', 'category_url'])

        Returns:
            None
    """
    parent_directory_name: str = 'Books'

    try:
        # Creates the parent directory with error handling
        os.mkdir(parent_directory_name)
        print('Directory ' + parent_directory_name + ' created successfully.')
    except FileExistsError:
        print('Directory ' + parent_directory_name + ' already exists.')
    except PermissionError:
        print('Permission denied: Unable to create ' +
              parent_directory_name + '.')
    except Exception as e:
        print('An error occurred: ' + e)

    # Creates a .txt file and writes every url in, then creates
    # a child directory with error handling
    with open('Books/category_urls_output.txt', 'w') as file_txt:
        for category_data in extracted_category_data:
            file_txt.write(category_data['category_url'] + '\n')
            nested_directory: str = parent_directory_name + \
                '/' + category_data['category_name']
            try:
                os.mkdir(nested_directory)
                print('Nested directories ' +
                      nested_directory + ' created successfully.')
            except FileExistsError:
                print('One or more directories in ' +
                      nested_directory + ' already exist.')
            except PermissionError:
                print('Permission denied: Unable to create ' +
                      nested_directory + '.')
            except Exception as e:
                print('An error occurred: ' + e)


def extract_article_urls(url: str) -> list[str]:
    """
    This function scraps the page(s) of each category
    and fetches the url of every book
    Returns a list of every book's url of the category as a string

        Parameters:
            url (str): the string of the category's url

        Returns:
            article_urls (list): the list of each book's url as a string

    """
    # Intance of object type list to hold all urls
    article_urls: list = []
    response_1 = requests.get(url)
    # Verification of web page connection
    if response_1.status_code == 200:
        # Instance of object type BeautifulSoup
        soup = BeautifulSoup(response_1.content, 'html.parser')
        # Checks if this is the only page
        if not soup.find('ul', class_='pager'):
            # Getting every article url in the page
            for li in soup.find_all(
                    'li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'):
                link: str = li.find('h3').find('a')['href'][9:]
                article_urls.append(link)

        else:
            # Getting rid of index.html and replacing it by page-i.html
            i = 1
            url_category_page: str = url[:-10] + 'page-' + str(i) + '.html'
            # Instance of object type requests.models.Response
            response_2 = requests.get(url_category_page)
            # Checking that the page exists
            while response_2.status_code != 404:
                # Verification of web page connection
                if response_2.status_code == 200:
                    # Instance of object type BeautifulSoup
                    soup = BeautifulSoup(response_2.content, 'html.parser')
                    # Getting every article url in the page
                    for li in soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'):
                        link: str = li.find('h3').find('a')['href'][9:]
                        article_urls.append(link)
                    # Go to next page
                    i += 1
                    url_category_page: str = url[:-10] + \
                        'page-' + str(i) + '.html'
                    response_2 = requests.get(url_category_page)

    return article_urls


def get_article_data(name_of_category: str) -> list[dict]:
    """
    This function scraps the page of a book and extracts
    all required information.
    It also dowloads the book's cover as a name_of_the_book.jpg
    image and saves it into the appropriate directory.
    Returns a list of dictionaries containing all the required
    information on the book page.

        Parameters:
            name_of_category (str): the book category that will be scraped

        Returns:
            extracted_article_data (list[dict]): the list of dictionaries
            containing all the required information on the book
            dict_keys(['product_page_url', 'title', 'review_rating',
            'product_description', 'image_url', 'category', 'upc',
            'product type', 'price (excl. tax)', 'price (incl. tax)',
            'tax', 'availability', 'number of reviews'])

    """
    # Instance of object type list, that will contain
    # a dictionary of data per book
    extracted_article_data: list[dict] = []
    # Opening the file.txt listing every book url
    # in the category
    with open('Books/' + name_of_category + '/' +
              name_of_category + '_book_urls.txt', 'r') as file_txt:
        for row in file_txt:
            # Le goulot est là (en termes de rapidité d'exécution)
            response = requests.get(row.strip())
            # response.encoding = "utf-8"
            # Checking website connection
            if response.status_code == 200:
                # Instance of the dictionary that will contain
                # all data and be appended to the list
                extracted_data: dict = {}
                # Data extraction
                extracted_data['product_page_url'] = row.strip()
                article_soup = BeautifulSoup(
                    response.content, 'html.parser', from_encoding='utf-8')
                extracted_data['title'] = article_soup.find(
                    'article').find('h1').string
                extracted_data['review_rating'] = article_soup.find(
                    'div', class_='col-sm-6 product_main').find_all(
                        'p')[2]['class'][1]
                extracted_data['product_description'] = article_soup.find(
                    'article').find_all('p')[3].string
                extracted_data['image_url'] = url + \
                    article_soup.find('article').find('img')['src'][6:]
                extracted_data['category'] = article_soup.find('ul').find_all(
                    'li')[2].find('a').string
                trs = article_soup.find_all('tr')
                for tr in trs:
                    for (th, td) in zip(tr.find_all('th'), tr.find_all('td')):
                        extracted_data[th.string.lower()] = td.string
                # Downloading image file
                # Instance of a variable to store content from the image url
                image_content = requests.get(
                    extracted_data['image_url']).content
                # Instance of a variable to create a byte object
                # from the url content
                image_file = io.BytesIO(image_content)
                # Instance of a variable to convert the byte object
                # into an RGB image
                image = Image.open(image_file).convert('RGB')
                # Saving the RGB image in the relative and
                # appropriate directory
                file_path_name_format: str = 'Books/' + name_of_category + \
                    '/' + extracted_data['title'].replace('/', '_') + '.jpg'
                image.save(file_path_name_format)

                # Adding the dictionary of the book information to the list
                extracted_article_data.append(extracted_data)

    return extracted_article_data


def transform_article_data(data_to_transform:
                           list[dict]) -> list[dict]:
    """
    This function transforms the extracted book data to better suit
    our requirements.
    Renames the dictionary keys to prepare for csv headers, deletes
    special caracters or unnecessary content.
    Converts numbers from string to int or float.
    Converts the review rating from string to integer by calling
    another function.
    Returns a list of dictionaries containing all the required transformed
    information on the book page.

        Parameters:
            data_to_transform (list[dict]): the list of dictionaries
            containing all the required information on the book.
            dict_keys(['product_page_url', 'title', 'review_rating',
            'product_description', 'image_url', 'category', 'upc',
            'product type', 'price (excl. tax)', 'price (incl. tax)',
            'tax', 'availability', 'number of reviews'])

        Returns:
            transformed_article_data (list[dict]): the list
            of dictionaries containing all the required transformed
            information of the books.
            dict_keys(['product_page_url', 'universal_product_code',
            'title', 'price_including_tax', 'price_excluding_tax',
            'number_available', 'product_description', 'category',
            'review_rating','image_url'])

    """
    transformed_article_data: list[dict] = []
    for data in data_to_transform:
        # Instance of a dictionary that will contain all the
        # transformed data and then be appended to the list
        transformed_data: dict = {}
        transformed_data['product_page_url'] = data['product_page_url']
        transformed_data['universal_product_code'] = data['upc']
        transformed_data['title'] = data['title']
        # Removal of the £ symbol and conversion into a float
        transformed_data['price_including_tax'] = float(
            data['price (incl. tax)'][1:])
        transformed_data['price_excluding_tax'] = float(
            data['price (excl. tax)'][1:])
        # Extraction of the digits only in this string and conversion
        # into a integer
        transformed_data['number_available'] = int(
            re.findall(r'(\d+)', data['availability'])[0])
        transformed_data['product_description'] = data['product_description']
        transformed_data['category'] = data['category']
        # Calling a external function to convert the string rating
        # into an integer rating
        transformed_data['review_rating'] = rating_conversion(
            data['review_rating'])
        transformed_data['image_url'] = data['image_url']

        # Adding the dictionary to the list
        transformed_article_data.append(transformed_data)

    return transformed_article_data


def load_article_data(data_to_load: list[dict], name_of_category: str) -> int:
    """
    This function reads through a list of dictionaries and creates a .csv
    file in the appropriate directory in order to
    write each dictionary as a row of the .csv file.
    The header is the list of the dictionaries' keys.
    Returns an integer (for debugging purposes) corresponding to the number
    of dictionaries whose values has been writen into the .csv file.

        Parameters:
            data_to_load (list[dict]): the list of dictionaries containing
            all the required transformed information of the books.
            dict_keys(['product_page_url', 'universal_product_code',
            'title', 'price_including_tax', 'price_excluding_tax',
            'number_available', 'product_description', 'category',
            'review_rating', 'image_url'])
            name_of_category (str) : name of the category that is being scraped

        Returns:
            number_of_books (int) : an integer corresponding to the number
            of books whose data has been writen in the .csv file.

    """
    # Creates a .csv file in the appropriate directory and writes
    # each dictionary of the list as a line
    with open('Books/' + name_of_category + '/' + name_of_category +
              '_book_data.csv', 'w', newline='') as file_csv:
        # Getting the header from the keys of the dictionary
        header: list[str] = (data_to_load[0].keys())
        # Instance of object type DictWriter
        writer = csv.DictWriter(file_csv, fieldnames=header)
        # Writing the header
        writer.writeheader()
        # Instance of the book counter
        number_of_books: int = 0
        # Writing each dictionary of the list as a row of the .csv file
        for row in data_to_load:
            writer.writerow(row)
            number_of_books += 1
        print(f'{number_of_books} books loaded.')

    return number_of_books


def load_article_urls(urls_to_load: list[str], name_of_category: str) -> None:
    """
    This function writes in a .txt file the list of each book's url.
    A row is equivalent to an url.
    The first parameter is the list of strings to be writen in the .txt file
    Returns nothing

        Parameters:
            urls_to_load (list[str]): the list of each book's url as a string
            name_of_category (str) : name of the category that is being scraped

        Returns:
            None

    """
    # Creates a .txt file in the appropriate directory in order to write
    # an url on a row of the file
    with open('Books/' + name_of_category + '/' + name_of_category +
              '_book_urls.txt', 'w') as file_txt:
        for row in urls_to_load:
            file_txt.write(url + 'catalogue/' + row + '\n')


def rating_conversion(rating_as_text: str = 'none') -> int:
    """
    This function converts the string passed as a parameter into an integer
    Returns the integer matching the conversion

        Parameters:
            rating_as_text (str): the string of the rating

        Returns:
            rating_as_number (int): the integer of the rating

    """
    rating_as_number = 0
    match rating_as_text:
        case 'One':
            rating_as_number = 1
        case 'Two':
            rating_as_number = 2
        case 'Three':
            rating_as_number = 3
        case 'Four':
            rating_as_number = 4
        case 'Five':
            rating_as_number = 5
        case _:
            rating_as_number = 999

    return rating_as_number


# Main

category_data_to_load = extract_category_data(url)
create_directories_and_urls_file(category_data_to_load)
category_number = 1
book_number = 0

for category_data in category_data_to_load:
    print('In category n°' + str(category_number) + ':')
    article_urls_to_load = extract_article_urls(category_data['category_url'])
    load_article_urls(article_urls_to_load, category_data['category_name'])
    article_data_to_transform = get_article_data(
        category_data['category_name'])
    article_data_to_load = transform_article_data(article_data_to_transform)
    books_loaded = load_article_data(
        article_data_to_load, category_data['category_name'])
    book_number = book_number + books_loaded
    category_number += 1

print('Script finished with ' + str(book_number) + ' books loaded.')
