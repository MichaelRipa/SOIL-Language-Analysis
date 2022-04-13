#! /usr/bin/env python3

'''scraper.py - Contains code for scraper used (specifically) for obtaining newspaper articles from "La repubblica" website '''

from random import randint,random,shuffle
import requests
import bs4
from time import sleep

URL = 'https://ricerca.repubblica.it/repubblica/archivio/repubblica/'

class Scraper:

    def generate_random_url(n=1,min_year=2000,max_year=2020):
        '''Randomly returns n urls with dates that fall between min_year and max_year. By default, the function returns all possible dates'''

        new_url = URL
        urls = []
        for year in range(min_year,max_year+1):
            for month in range(1,13):
                for day in range(1,29):
                    urls.append(new_url + str(year) + '/' + str(month) + '/' + str(day))

        shuffle(urls)
        if n == None:
            return urls

        return urls[0:n]


    def _grab_article_link(article):
        
        header = ''
        
        #This method of iterating through the articles children is more robust, as article.get() does not work on certain pages

        for tag in article.children: 
            if tag.name == 'h1':
                header = tag
            elif tag.name == 'p':
                for sub_tag in tag.children:
                    if sub_tag.name == 'span':
                        try:
                            if 'typefoto' in sub_tag.get('class'):
                                return [] # Filters out non-text media articles 
                        # This may lead to more true negatives
                        except:
                            pass

        if header != '':
            for tag in header.children:
                if tag.name == 'a':
                    if tag.get('title') == "Leggi l'articolo":
                        return [tag.get('href')] 

        return [] # Couldn't find the hyperlink




    def scrape_articles(url=None):
        '''For a given url of a specific days news articles, returns allhyperlinks on the page that link to (text based) articles'''                
        if url == None:
            url = Scraper.generate_random_url()

        req = requests.get(url)

        assert req.status_code == 200
        
        soup = bs4.BeautifulSoup(req.text,'html.parser')
        links = []

        for article in soup.find_all('article'):
            links += Scraper._grab_article_link(article)

        return links
            
    def scrape_page(url=None):
        '''For a provided url to a news article, scrapes all text obtained from the page'''

        assert url != None

        req = requests.get(url)

        assert req.status_code == 200
        
        soup = bs4.BeautifulSoup(req.text,'html.parser')

        article_div = ''
        article_text = ''

        for div in soup.find_all('div'):

            if div.get('id') != None:
                if div.get('id') in ['article-body','article']:
                    article_div = div
                    break

            if div.get('class') != None:
                if div.get('class') in ['story__text','articolo']:
                    article_div = div
                    break


        if article_div == '':
            return ''
        # May be worthwhille doing clean-up here
        for line in article_div.stripped_strings:
            article_text += line + ' '

        return article_text

        
    
    def scrape_pipeline(n=10):
        ''' For an inputted input n, returns text scrapped from 10 valid articles'''
        
        assert type(n) == int
        assert n > 0

        remaining_articles = n
        raw_text = ''
        urls = generate_random_url()
        i = 0
        
        while remaining_articles > 0:
            
            # Grab article hyperlinks for arbitrary date
            new_articles = scrape_articles(urls[i])
            i += 1
            for article in new_articles:
                sleep(random()) # Avoid overloading the server
                article_text = scrape_article(article)
                if article_text != '':
                    raw_text += ' ' + article_text 
                    remaining_articles -= 1

        
        
        return raw_text


         
