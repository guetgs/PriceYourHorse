import os
import numpy as np
from bs4 import BeautifulSoup
from pymongo import MongoClient
from web_scraping import initiate_database

DB_NAME = 'horse_ads_database'
TABLE_NAME = 'horse_features_all'
ADS_PATH = '../data/ads/'


def get_filename():
    '''
    INPUT: None
    OUTPUT: string

    Generator that yields all filenames present in
    the advertisement folder.
    '''
    for filename in os.listdir(ADS_PATH):
        if filename not in ['.DS_Store', 'horse-ad-.html']:
            yield filename


def get_content(filename):
    '''
    INPUT: string
    OUTPUT: string

    Opens file filename and returns content of the file.
    '''
    with open(ADS_PATH + filename) as f:
        return f.read()


def get_id(filename):
    '''
    INPUT: string
    OUTPUT: int

    Extracts article id from filename.
    '''
    return filename.split('-')[-1][:-5]


def extract_features(_id, content, table):
    '''
    INPUT: int, string, mongodb table
    OUTPUT: None

    Parses string and extracts relevant features into
    a dictionary that is stored in table.
    '''
    soup = BeautifulSoup(content, 'html.parser')
    h1 = soup.select('h1')[0].get_text()
    if h1 in ['This Ad Has Been Deleted', 'This Ad Is Unavailable']:
        return
    # define css selectors of fields containing desired features
    price_css = 'div.well.margin-bottom5.padding-bottom10 \
                 div.item-price.text-big.text-bold \
                 span.item-price.text-success'
    city_state_css = 'div.well.margin-bottom5.padding-bottom10 \
                      header \
                      h5.text-primary'
    titles_css = 'ul.meta-data.list-unstyled \
                  li dl.row \
                  dt.col-xs-5'
    features_css = 'ul.meta-data.list-unstyled \
                    li dl.row \
                    dd.col-xs-7'
    skills_css = 'div.well dl.row.margin-bottom0.padding-bottom10 \
                  dd.col-sm-10'
    description_css = 'div.col-sm-12.no-padding-xs \
                       div.well p \
                       span[itemprop=description]'
    pedigree_panel_css = 'div.panel.panel-primary \
                          div.panel-heading \
                          h3.panel-title'
    # extract features into dictionary
    data = {}
    data['_id'] = _id
    price = soup.select(price_css)
    if price:
        data['Price'] = price[0].get_text()
    city_state = soup.select(city_state_css)[0]\
                     .get_text().split(', ')
    data['City'] = city_state[0]
    if len(city_state) > 1:
        data['State'] = city_state[1]
    titles = soup.select(titles_css)
    features = soup.select(features_css)
    for i, title in enumerate(titles):
        data[title.get_text()] = features[i].get_text()
    skills = soup.select(skills_css)
    if skills:
        data['Skills / Disciplines'] = skills[0].get_text()
    data['Description'] = soup.select(description_css)[0]\
                              .get_text()
    if soup.select(pedigree_panel_css):
        data['Pedigree'] = 1
    else:
        data['Pedigree'] = 0

    table.insert_one(data)


def extract_all(table, verbose=True):
    '''
    INPUT: mongodb table, boolean
    OUTPUT: None

    Extracts features from all articles and stores them
    in table.
    '''
    n = 0
    for filename in get_filename():
        print filename
        content = get_content(filename)
        _id = get_id(filename)
        extract_features(_id, content, table)
        n += 1
        if verbose:
            if np.mod(n, 100) == 0:
                print '{} articles extracted ...'.format(n)


if __name__ == '__main__':
    table = initiate_database(DB_NAME, TABLE_NAME)
    extract_all(table)
