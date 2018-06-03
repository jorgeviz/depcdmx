"""
Module to scrape Lamudi DF appartments
and stores data in local storage as CSV.

Fetched Fields:
name, location, description, price, rooms, toilettes, surface, link 
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
from pprint import pprint as pp
import datetime as dt

# Vars
_base_url = "https://www.lamudi.com.mx/distrito-federal/departamento/for-sale/?page={}"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
ddir = 'data/'


def save(depts):
    """ Append page data

        Params:
        -----
        depts : list
            List of Departments
    """
    # Read file if exists
    _fname = ddir+"{}/inmuebles24.csv".format(dt.date.today().isoformat())
    try:
        df = pd.read_csv(_fname, delimiter='~')
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
            depdf.set_index(['name','location']).to_csv(_fname, sep='~')
            print('Correctly saved file: {}'.format(_fname))
        else:
            df = pd.concat([df, depdf])
            df.set_index(['name','location']).to_csv(_fname, sep='~')
            print('Correctly saved file: {}'.format(_fname))
    except Exception as e:
        print(e)
        print('Could not save file: {}'.format(_fname))


def scrape(content):
    """ Scrape all departments per page
         
        Params:
        -----
        content: str
            HTML content
    """
    data = []
    # Generate soup
    soup = BeautifulSoup(content, 'html.parser')
    with open(ddir+'lamudi.html', 'w') as _F:
        _F.write(soup.prettify())
    for d in soup.find_all(class_="card ListingCell-content"):
        _dept = {}
        _dept['name'] = d.find(class_="ListingCell-KeyInfo-title").text.strip()
        _dept['location'] = ' '.join(j.strip() for j in d.find(class_="ListingCell-KeyInfo-address ellipsis").text.strip().split('\n'))
        _dept['description'] = d.find(class_="ListingCell-shortDescription").text.strip().replace(u'\xa0', u'').replace('\n',' ')
        try:
            _dept['price'] = d.find(class_="PriceSection-FirstPrice").text.replace('$','').replace(',','').strip()
        except:
            try:
                _dept['price'] = d.find(class_="PriceSection-SecondPrice").text.replace('$','').replace(',','').replace('US','').strip()
            except Exception as e:
                _dept['price'] = ''
        _rooms, _toils, _surf = '-', '-', '-'
        for at in d.find_all(class_="KeyInformation-attribute"):
            _label = at.find(class_='KeyInformation-label').text.strip()
            _val = at.find(class_="KeyInformation-value").text.strip()
            if 'Rec' in _label:
                _rooms = _val
            elif 'Baño' in _label:
                _toils = _val
            elif 'Superf' in _label:
                _surf = _val
        _dept['rooms'],_dept['toilettes'],_dept['surface'] = _rooms, _toils, _surf
        _dept['link'] = d.find('a')['href']
        # Append Data
        data.append(_dept)    
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
            # Anti blocking delay
            time.sleep(random.randint(0,5))
            if r.status_code != 200:
                raise Exception("Wrong Response")
            depts = scrape(r.content)
            print('Found {} departments'.format(len(depts)))
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
    print('Starting to scrape Lamudi')
    pages = paginate()


if __name__ == '__main__':
    main()