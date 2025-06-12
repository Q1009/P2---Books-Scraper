# BOOKS SCRAPER
*(Books Online Monitoring Solution)*

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)

This script aims at scraping the <https://books.toscrape.com> website in order to gather specific data for analysis

## Get started

- Open your terminal and navigate through your desired directory using the 'cd' command line.

### Requirements

- Start by cloning the GitHub repository  
git clone http://
- Create your virtual environment  
python3 -m venv env

### Installation

- Activate your virtual environment  
`source env/bin/activate`  
- Install requirements  
`pip install -r requirements.txt`  

## Running

- Run the script
python main.py
- The execution runs for about 5 to 10 mins

## Data collection

You will then find a 'Books' directory in which sub directories, corresponding to every category of books, will contain the requested data:

- Books' illustrations
- A csv file containing :
    - product page url
    - universal product code
    - title
    - price including tax
    - price excluding tax
    - number available (in stock)
    - product description
    - category
    - review rating
    - image url

## Contributing

Si vous souhaitez contribuer, lisez le fichier [CONTRIBUTING.md](https://example.org) pour savoir comment le faire.

## Versions
Listez les versions ici 
_exemple :_
**Dernière version stable :** 5.0
**Dernière version :** 5.1
Liste des versions : [Cliquer pour afficher](https://github.com/your/project-name/tags)
_(pour le lien mettez simplement l'URL de votre projets suivi de ``/tags``)_

## Author

- **Quentin Tellier** _alias_ [@Q1009](https://github.com/Q1009)
