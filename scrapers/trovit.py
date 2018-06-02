"""
Module to scrape Segunda Mano DF appartments
and stores data in local storage as CSV.
"""

# Vars
_base_url = "https://casas.trovit.com.mx/index.php/cod.search_homes/type.1/what_d.Mexico/rooms_min.0/bathrooms_min.0/city.DF/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.{}"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"