#! /usr/bin/env python3

from random import randint
import requests
import bs4

URL = 'https://ricerca.repubblica.it/repubblica/archivio/repubblica/'

class Scraper:

    def generate_random_url(min_year=2000,max_year=2020):

        new_url = URL
        year = str(randint(min_year,max_year))
        month = str(randint(1,12))
        day = str(randint(1,28))

        if len(month) < 2:
            month = '0' + month

        if len(day) < 2:
            day = '0' + day

        return new_url + year + '/' + month + '/' + day


    def scrape_articles(url=None):
                
        if url == None:
            url = Scraper.generate_random_url()

        req = requests.get(url)

        assert req == 200
        
        soup = bs4.BeautifulSoup(req.text,'html.parser')
        links = []

        for article in soup.find_all('article'):
            # Will need to check that current article links to written news
            for link in article.find_all('a'):
                if link.get('title') == "Leggi l'articolo": 
                    
                    links.append(link.get('href'))

        
        

         
