import numpy as np
import requests
import pandas as pd
import datetime
import re
import pickle
import os
import threading
from bs4 import BeautifulSoup
from pymongo import MongoClient


def check_directory_structure():
    '''
    INPUT: None
    OUTPUT: None

    Checks if directories to store links and html pages are
    available and provides them if necessary.
    '''
    dirs = ['../data/',
            '../data/linklists/',
            '../data/ads/']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)


def save_linklists(url, start_page, delta_page):
    '''
    INPUT: string, int, int
    OUTPUT: int

    Calls scrap_linklist to save lists of links to advertisement
    detail pages containing delta_page links, starting from
    start_page. Returns the maximal number of search results
    pages.
    '''
    end_page = delta_page
    n_ads = scrap_linklist(url, start_page, end_page)
    print 'a total of {} ads found...'.format(n_ads)
    start_page += delta_page
    end_page += delta_page
    max_page = n_ads / 8
    n_lists = 1
    while end_page <= max_page:
        scrap_linklist(url, start_page, end_page)
        n_lists += 1
        print '{} lists done...'.format(n_lists)
        start_page += delta_page
        end_page += delta_page
    scrap_linklist(url, start_page, max_page)
    return max_page


def scrap_linklist(url, start_page, end_page):
    '''
    INPUT: string, int, int
    OUTPUT: int

    Extracts links to advertisement details pages from the search
    results pages given by input url and start_page to end_page and
    saves them as list. Returns the maximal number of search
    result pages.
    '''
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) \
                              AppleWebKit/537.36 (KHTML, like Gecko) \
                              Chrome/43.0.2357.130 Safari/537.36'}
    s.headers.update(headers)
    linklist = []
    z = s.get(url)
    soup = BeautifulSoup(z.content, 'html.parser')
    n_ads = int(soup.select('span.total-result-count')[0]
                    .get_text().replace(',', ''))
    for page in xrange(start_page, end_page):
        page_url = url + '?pg={}'.format(page)
        z = s.get(page_url)
        soup = BeautifulSoup(z.content, 'html.parser')
        details = soup.select('a.btn.btn-primary.btn-sm')
        for d in details:
            if d['href'][:20] == 'http://www.equinenow':
                linklist.append(d['href'])
        if np.mod(page, 20) == 0:
            print '{} pages scanned...'.format(page)
    filename = '../data/linklists/linklist_{}_{}'.format(start_page, end_page)
    with open(filename, 'wb') as f:
        pickle.dump(linklist, f)
    return n_ads


def load_linklists(start_page, delta_page, max_page):
    '''
    INPUT: int, int, int
    OUTPUT: set

    Loads and merges all lists of links saved by save_linklists,
    saves the merged list on disk and returns a set with unique links.
    '''
    end_page = delta_page
    linklist = []
    while end_page <= max_page:
        filename = '../data/linklists/linklist_{}_{}'\
                   .format(start_page, end_page)
        with open(filename, 'rb') as f:
            linklist.extend(pickle.load(f))
        start_page += delta_page
        end_page += delta_page
    filename = '../data/linklists/linklist_{}_{}'.format(start_page, max_page)
    with open(filename, 'rb') as f:
        linklist.extend(pickle.load(f))
    return set(linklist)


def initiate_database(db_name, table_name):
    '''
    INPUT: string, string
    OUTPUT: mongodb table

    Connects to mongodb database db_name and table table_name through
    pymongo and returns handle to table.
    '''
    client = MongoClient()
    db = client[db_name]
    table = db[table_name]
    return table


def update_database(url, table):
    '''
    INPUT: list, string, mongodb table
    OUTPUT: None

    Scrapes search results pages, compares the links to the list of already
    present links and scrapes advertisement detail pages for links not yet
    present in the list of links. Updates the list of links to contain all
    links of already scraped detail pages.
    '''
    if os.path.isfile('../data/linklists/complete_linklist'):
        with open('../data/linklists/complete_linklist', 'rb') as f:
            linklist = pickle.load(f)
    else:
        linklist = load_linklists(0, 100, 10154)
    start_page = 0
    delta_page = 25
    end_page = delta_page
    something_new = True
    while something_new:
        n_ads = scrap_linklist(url, start_page, end_page)
        filename = '../data/linklists/linklist_{}_{}'\
                   .format(start_page, end_page)
        with open(filename) as f:
            new_links = pickle.load(f)
        new_links = [link for link in new_links if link not in linklist]
        if new_links == []:
            print 'nothing new after {} pages'.format(end_page)
            something_new = False
            break
        t = []
        for i, link in enumerate(new_links):
            t.append(threading.Thread(target=scrap_one, args=(link, table)))
            t[i].start()
        for thread in t:
            thread.join()
        start_page += delta_page
        end_page += delta_page
        linklist.update(new_links)
    with open('../data/linklists/complete_linklist', 'wb') as f:
        pickle.dump(linklist, f)


def scrap_one(url, table):
    '''
    INPUT: string, mongodb table
    OUTPUT: None

    Scrapes advertisement detail page given by url, saves the whole page
    to disk, extracts relevant features and stores them into the mongodb
    table provided as input parameter.
    '''
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) \
                              AppleWebKit/537.36 (KHTML, like Gecko) \
                              Chrome/43.0.2357.130 Safari/537.36'}
    s.headers.update(headers)
    ad = '../data/ads/' + url.split('/')[-1] + '.html'
    content = s.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    h1 = soup.select('h1')[0].get_text()
    if not h1 == 'This Ad Has Been Deleted':
        with open(ad, 'w') as f:
            f.write(content)
        try:
            data = {}
            price_css = 'div.well.margin-bottom5.padding-bottom10 \
                         div.item-price.text-big.text-bold \
                         span.item-price.text-success'
            price = soup.select(price_css)
            if price:
                data['price'] = price[0].get_text()
            city_state = soup.select('h5.text-primary')[0]\
                             .get_text().split(', ')
            data['city'] = city_state[0]
            if len(city_state) > 1:
                data['state'] = city_state[1]
            titles = soup.select('dt.col-xs-5')
            contents = soup.select('dd.col-xs-7')
            for i, t in enumerate(titles):
                data[t.get_text()] = contents[i].get_text()
            skills = soup.select('dd.col-sm-10')
            if skills:
                data['Skills / Disciplines'] = skills[0].get_text()
            data['additional comments'] = soup.select('span[itemprop=\
                                                       description]')[0]\
                                              .get_text()
            if soup.select('h3.panel-title'):
                data['pedigree'] = 1
            else:
                data['pedigree'] = 0
            table.insert_one(data)
        except IndexError:
            print 'problem: ' + url


def scrap_many(linklist, table, start_link):
    '''
    INPUT: list, mongodb table, int
    OUTPUT: None

    Calls scrape_one to scrape individual advertisement detail pages
    for all links in linklist starting at the link with index
    start_link.
    '''
    print '{} links to process'.format(len(linklist))
    for i, ll in enumerate(linklist[start_link:]):
        scrap_one(ll, table)
        if np.mod(i, 100) == 0:
            print '{} links processed...'.format(i + start_link)


def run_from_scratch(url, table):
    '''
    INPUT: string, mongodb table
    OUTPUT: None

    Calls different functions to scrape links to detail pages
    from url, scrape these detail pages and store
    extracted features in the mongodb table provided as input
    parameter.
    '''
    start_page = 0
    delta_page = 100
    max_page = save_linklists(url, start_page, delta_page)
    linklist = load_linklists(start_page, delta_page, max_page)
    scrap_many(linklist, table, 0)


def continue_at_custom_link(url, table, current_link):
    '''
    INPUT: string, mongodb table, int
    OUTPUT: None

    Continues scraping detail pages starting from the link
    indexed by current_link and stores extracted features
    in table.
    '''
    max_page = 10154
    linklist = load_linklists(start_page, delta_page, max_page)
    print linklist[current_link]
    scrap_many(linklist, table, current_link)


if __name__ == '__main__':
    url = 'http://www.equinenow.com/horses.htm'
    check_directory_structure()
    table = initiate_database(db_name='horse_ads_database',
                              table_name='horse_info')

    # run_from_scratch(url, table)

    # current_link = 75091 # link at which to continue scraping
    # continue_at_custom_link(url, table, current_link)

    #     version to update database with results previously not present
    update_database(url, table)
