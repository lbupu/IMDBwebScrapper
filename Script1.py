# Web scrapping example


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn

names = []
years = []
imdb_ratings = []
metascores = []
votes = []

years_url = [str(i) for i in range(2000,2018)]
pages = [str(i) for i in range(1,5)]

start_time = time()
requests = 0

#Loop en la lista de peliculas por año
for year_url in years_url:

    #Loop en las cuatro primeras paginas de peliculas de un año
    for page in pages:
        #Request de la url "dinámica"
        url = 'http://www.imdb.com/search/title?release_date='+year_url+'&sort=num_votes,desc&page='+page
        response = get(url)

        # Pause the loop
        sleep(randint(8, 15))

        # Monitorizacion de requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        clear_output(wait=True)

        # Si recibimos un respuetsa diferente a 200, throw warning
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop si el numero de request mayor de 72
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        #BS parse y find todos los "movie containers"
        html_soup = BeautifulSoup(response.text, 'html.parser')
        movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

        #Loop en el parse. Buscamos los atributos (Name, year, rating, metascore y vote) y lo guardamos en una lista
        for container in movie_containers:
            if container.find('div', class_ = 'ratings-metascore') is not None:
                name = container.h3.a.text
                names.append(name)
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                years.append(year)
                imdb_rating = float(container.find('div', class_ = 'lister-item-content').div.div.strong.text)
                imdb_ratings.append(imdb_rating)
                metascore = container.find('span', class_='metascore').text
                metascores.append(metascore)
                vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
                votes.append(vote)



movie_ratings = pd.DataFrame({'movie': names,
                       'year': years,
                       'imdb': imdb_ratings,
                       'metascore': metascores,
                       'votes': votes})
print(movie_ratings.info())
print(movie_ratings.head(10))


