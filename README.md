# CDMX Selling Appartment prices

Scrapes data from following sites:

- <www.lamudi.com.mx>
- <www.inmuebles24.com>
- <www.segundamano.mx>
- <casas.trovit.com.mx>
- <propiedades.com>

to retrieve info from Distrito Federal (DF) appartments in sale.

Stores historical data in local storage and has a visualization
notebook to verify best deals.

## How to run it?

Install requirements:

```bash
pip install -r requirements.txt
```

Run each scraper individually

```bash
# Inmuebles24
python scrapers/inmuebles24.py

# Lamudi 
python scrapers/lamudi.py

# ...
```

Best deals' data analysis is in the `notebooks/Delegation Analysis.ipynb` jupyter notebook file.



## License

[MIT License](./LICENSE)


## TODO

- JS for Lamudi
- Segunda Mano Scraper
- Trovit Scraper
- Propiedades Scraper
- Analysis Notebook extended
