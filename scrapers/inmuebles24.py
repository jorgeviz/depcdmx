"""
Module to scrape Inmuebles 24
and stores data in local storage as CSV.

Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
import requests
import statistics
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import os

# Vars
_root = 'https://www.inmuebles24.com/'
_state = 'nuevo-leon'
_operation = 'venta'
_base_url = _root + "inmuebles-en-" + _operation + "-en-" + _state + "-pagina-{}.html"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
ddir = 'data/'


def save(depts):
    """ Append page data

        Params:
        -----
        depts : pd.Dataframe()
            Dataframe of Departments
    """
    # Read Existant file to append
    _fname = ddir + "{}/inmuebles24" + "-" + _state + "-" + _operation + ".csv"
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
    for d in soup.find_all(class_="posting-card"):
        temp_dict = {}
        try:
            temp_dict['name'] = d.find(class_="posting-title").text.strip()
            temp_dict['description'] = d.find(class_="posting-description").text.strip()
            temp_dict['location'] = ' '.join([j.strip() for j in d.find(class_="posting-location").text.strip().split('\n')])
            temp_dict['link'] = d.find(class_="posting-title").find('a').get('href')
            temp_dict['price'] = d.find(class_="first-price").text.strip()
            temp_dict['operation'] = _operation
            for li in d.find(class_="main-features").findAll('li'):
                li = li.text.lower()
                if 'recámara' in li:
                    temp_dict['rooms'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
                elif 'baño' in li:
                    temp_dict['bathrooms'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
                elif 'construido' in li:
                    temp_dict['construction (m2)'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
                elif 'terreno' in li:
                    temp_dict['terrain (m2)'] = statistics.mean([int(s) for s in li.split() if s.isdigit()])
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
                             headers={'user-agent': user_agent})
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
    print('Starting to scrape Inmuebles24')
    paginate()
    return "Done"


if __name__ == '__main__':
    main()
