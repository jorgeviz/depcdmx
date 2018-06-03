"""
Module to scrape Segunda Mano DF appartments
and stores data in local storage as CSV.
"""
import requests
import pandas as pd
from pprint import pprint as pp
from bs4 import BeautifulSoup

# Vars
_base_url = "https://propiedades.com/df/departamentos?pagina={}"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
ddir='data/'

def save(depts):
    """ Append page data

        Params:
        -----
        depts : list
            List of Departments
    """
    # Read Existant file to append
    _fname = ddir+"{}/propiedades.csv".format(dt.date.today().isoformat())
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
    """
    data = []
    # Generate soup
    soup = BeautifulSoup(content, 'html.parser')
    with open(ddir+'propiedades.html', 'w') as _F:
        _F.write(soup.prettify())
    # Get Characteristics
    for d in soup.find_all(class_="ad"):
        print('----')
        try:
            print(d) 
        except Exception as e:
            print(e)
            continue
        break
    print('Found {} depts'.format(len(data)))
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
        #save(depts)
        pg_nums += 1
        break ###
    return pg_nums

def main():
    """ Main method
    """
    print('Starting to scrape Inmuebles24')
    pages = paginate()


if __name__ == '__main__':
    main()