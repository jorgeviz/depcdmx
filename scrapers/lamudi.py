"""
Module to scrape Lamudi DF appartments
and stores data in local storage as CSV.

Fetched Fields:
name, location, description, price, rooms, toilettes, surface, link 
"""
import requests
import pandas as pd

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
    pass


def scrape(content):
    """ Scrape all departments per page
    """
    data = []
    # Generate soup
    soup = 
    return data

def paginate():
    """ Loop over pages to retrieve all info available

        Returns:
        -----
        pg_nums : int
            Number of pages scraped
    """
    pg_nums = 0
    while True:
        try:
            r = requests.get(url.format(pg_nums),
                headers={'user-agent': user_agent})
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
    return pg_nums

def main():
    """ Main method
    """
    print('Starting to scrape')
    pages = paginate()


if __name__ == '__main__':
    main()