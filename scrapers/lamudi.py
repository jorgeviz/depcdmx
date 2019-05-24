"""
Module to scrape Lamudi
and stores data in local storage as CSV.

Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
import requests
import statistics
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import random
import time
import os

# Vars
_root = "https://www.lamudi.com.mx/"
_state = 'nuevo-leon'
_operation = 'venta'
_base_url = _root + _state + "/for-sale/?page={}"
ddir = 'data/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referrer': 'https://google.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache',
}


def save(depts):
    """ Append page data

        Params:
        -----
        depts : pd.Dataframe()
            Dataframe of Departments
    """
    # Read Existant file to append
    _fname = ddir + "{}/lamudi" + "-" + _state + "-" + _operation + ".csv"
    _fname = _fname.format(dt.date.today().isoformat())
    try:
        df = pd.read_csv(_fname, delimiter=',')
    except:
        print('New file, creating folder..')
        try:
            os.mkdir(ddir + '{}'.format(dt.date.today().isoformat()))
            print('Created folder!')
        except:
            print('Folder exists already!')
        df = pd.DataFrame()
    # Append data
    print(depts.head(1).to_dict())
    try:
        if df.empty:
            depts.set_index(['name', 'location']).to_csv(_fname, sep=',')
            print('Correctly saved file: {}'.format(_fname))
        else:
            df = pd.concat([df, depts])
            df.set_index(['name', 'location']).to_csv(_fname, sep=',')
            print('Correctly saved file: {}'.format(_fname))
    except Exception as e:
        print(e)
        print('Could not save file: {}'.format(_fname))


def scrape(content):
    """ Scrape all listings per page """
    columns = ['name',
               'description',
               'location',
               'link',
               'price',
               'operation',
               'rooms',
               'bathrooms',
               'construction (m2)',
               'terrain (m2)']

    data = pd.DataFrame(columns=columns)
    # Generate soup
    soup = BeautifulSoup(content, 'html.parser')
    # Get Characteristics
    for d in soup.find_all(class_="ListingCell-AllInfo"):
        temp_dict = {}
        try:
            temp_dict['name'] = d.find(class_="ListingCell-KeyInfo-title").text.strip()
            temp_dict['description'] = d.find(class_="ListingCell-shortDescription").text.strip()
            temp_dict['location'] = ' '.join([j.strip() for j in d.find(class_="ListingCell-KeyInfo-address").text.strip().split('\n')])
            temp_dict['link'] = d.find(class_="ListingCell-KeyInfo-title").find('a').get('href')
            temp_dict['price'] = d.find(class_="PriceSection-FirstPrice").text.strip()
            temp_dict['operation'] = _operation
            for att in d.find(class_="KeyInformation").find_all(class_="KeyInformation-attribute"):
                att = att.text.lower()
                if 'recámara' in att:
                    temp_dict['rooms'] = statistics.mean([int(s) for s in att.split() if s.isdigit()])
                elif 'baño' in att:
                    temp_dict['bathrooms'] = statistics.mean([int(s) for s in att.split() if s.isdigit()])
                elif 'terreno' in att:
                    temp_dict['terrain (m2)'] = statistics.mean([int(s) for s in att.split() if s.isdigit()])
                elif 'superficie' in att:
                    temp_dict['construction (m2)'] = statistics.mean([int(s) for s in att.split() if s.isdigit()])
        except Exception as e:
            print(e)
            continue
        data = data.append(temp_dict, ignore_index=True)
    print('Found {} depts'.format(len(data['name'])))
    return data


def paginate():
    """ Loop over pages to retrieve all info available

        Returns:
        -----
        pg_nums : int
            Number of pages scraped
    """
    pg_nums = 1
    while True:
        try:
            print(_base_url.format(pg_nums))
            r = requests.get(_base_url.format(pg_nums),
                             headers=headers)
            # Anti blocking delay
            time.sleep(random.randint(5, 10))
            if r.status_code != 200:
                raise Exception("Wrong Response")
            depts = scrape(r.content)
            if depts.empty:
                raise Exception("No more departments")
        except Exception as e:
            print(e)
            print('Finishing to retrieve info.')
            break
        # Store values
        save(depts)
        pg_nums += 1
    return pg_nums


def main():
    """ Main method """
    print('Starting to scrape Lamudi')
    paginate()
    return "Done"


if __name__ == '__main__':
    main()
