"""
Module to scrape Inmuebles 24 DF appartments
and stores data in local storage as CSV.

Fetched Fields:
name, location, description, price, rooms, toilettes, surface, link 
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint as pp
import datetime as dt
import os

# Vars
_base_url = "https://www.inmuebles24.com/departamentos-en-venta-en-distrito-federal-pagina-{}.html"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
ddir = 'data/'


def save(depts):
    """ Append page data

        Params:
        -----
        depts : list
            List of Departments
    """
    # Read Existant file to append
    _fname = ddir+"{}/inmuebles24.csv".format(dt.date.today().isoformat())
    try:
        df = pd.read_csv(_fname)
    except:
        print('New file, creating folder..')
        try:
            os.mkdir(ddir+'{}'.format(dt.date.today().isoformat()))
            print('Created folder!')
        except:
            print('Folder exists already!')
        df = pd.DataFrame()
    # Append data
    depdf = pd.DataFrame(depts)
    print(depdf.head(1).to_dict())
    try:
        if df.empty:
            depdf.to_csv(_fname)
            print('Correctly saved file: {}'.format(_fname))
        else:
            df = pd.concat([df, depdf])
            depdf.reset_index(drop=True).to_csv(_fname)
            print('Correctly saved file: {}'.format(_fname))
    except Exception as e:
        print(e)
        print('Could not save file: {}'.format(_fname))


def scrape(content):
    """ Scrape all departments per page
    """
    data = {
        'name': [],
        'description': [],
        'location':[],
        'link': [],
        'price': [],
        'rooms': [],
        'surface': []
        }
    # Generate soup
    soup = BeautifulSoup(content, 'html.parser')
    #with open(ddir+'inmuebles24.html', 'w') as _F:
    #    _F.write(soup.prettify())
    # Get Characteristics
    for d in soup.find_all(class_="aviso-data aviso-data--right"):
        try:
            data['name'].append(d.find(class_="dl-aviso-a").text.strip())
            data['description'].append(d.find(class_="aviso-data-description dl-aviso-link ").text.strip())
            data['location'].append(' '.join([j.strip() for j in d.find(class_="aviso-data-location dl-aviso-link").text.strip().split('\n')]))
            data['link'].append("https://www.inmuebles24.com"  + d.find(class_="dl-aviso-a")['href'])
            _rooms, _surf = '-', '-'
            for f in d.find_all(class_="aviso-data-features-value"):
                _val = f.text
                if 'Rec.' in _val:
                    _rooms = _val.split('\n')[0].strip()
                elif 'm²' in _val:
                    _surf = _val.strip().split('\n')[0].strip()
            data['rooms'].append(_rooms)
            data['surface'].append(_surf)   
        except Exception as e:
            print(e)
            continue
    # Get Prices
    for d in soup.find_all(class_="aviso-data-price"):
        _price = ''
        try:
            _price = d.find(class_="aviso-data-price-value ")\
                .text.replace('MN','').replace(',','').replace('U$D','').strip()
        except:
            try:
                _price = d.find(class_="aviso-data-price-value")\
                    .text.replace('MN','').replace(',','').replace('U$D','').strip()
            except Exception as e:
                print(e)
        data['price'].append(_price)
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
            if not depts:
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
    """ Main method
    """
    print('Starting to scrape Inmuebles24')
    pages = paginate()


if __name__ == '__main__':
    main()