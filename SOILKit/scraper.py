#! /usr/bin/env python3

'''scraper.py - Contains code for scraper used (specifically) for obtaining newspaper articles from "La repubblica" website '''

from random import randint,random,shuffle
import requests
import bs4
import re
import datetime
from time import sleep

URL = 'https://ricerca.repubblica.it/repubblica/archivio/repubblica/'
PROXY_URL = 'https://free-proxy-list.net/'

class Scraper:

    def generate_all_urls(start_year=2010,end_year=2017,start_month=1,end_month=12,start_day=1,end_day=31):
        '''Generates urls for all valid dates between start_year - start_month - start_day to end_year - end_month - end_day'''

        new_url = URL
        urls = []
        for year in range(start_year,end_year+1):
            for month in range(start_month,end_month+1):
                for day in range(start_day,end_day+1):
                    try:
                        date = datetime.date(year,month,day)
                        
                        urls.append(new_url + date.isoformat().replace('-','/'))
                    except:
                        pass
        return urls


    def _get_proxies():
        '''Scrapes a list of proxies to be used with pipeline'''
        req = requests.get(PROXY_URL)
        assert req.status_code == 200

        soup = bs4.BeautifulSoup(req.text,'html.parser')
        proxies = re.findall(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+',str(soup))
        return proxies


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


    def _get_page_contents(soup):

        article_div = ''
        article_text = ''

        for div in soup.find_all('div'):

            if div.get('id') != None:
                if div.get('id') in ['article-body','article']:
                    article_div = div
                    break

            if div.get('class') != None:

                if div.get('class')[0] in ['story__text','articolo']:
                    article_div = div
                    break

                #Note: for some reason get('class') returns a list while get('div') returns a string

        if article_div == '':
            return ''
        # May be worthwhille doing clean-up here
        for line in article_div.stripped_strings:
            article_text += line + ' '

        return article_text



    def scrape_articles(url=None):
        '''For a given url of a specific days news articles, returns allhyperlinks on the page that link to (text based) articles'''                
        if url == None:
            url = Scraper.generate_random_url()

        req = requests.get(url)

        if req.status_code != 200:
            print('Following url gave ' + str(req.status_code) + ' status code: ' + str(url))
            return [] 

        soup = bs4.BeautifulSoup(req.text,'html.parser')
        links = []

        for article in soup.find_all('article'):
            links += Scraper._grab_article_link(article)

        return links
            
    def scrape_page(url=None):
        '''For a provided url to a news article, scrapes all text obtained from the page'''

        assert url != None

        req = requests.get(url)
        req.encoding = 'UTF-8' # Omitting this leads to certain characters not showing up correctly

        if req.status_code != 200:
            print('Following url gave ' + str(req.status_code) + ' status code: ' + str(url))
            return '' 

        
        soup = bs4.BeautifulSoup(req.text,'html.parser')
        return Scraper._get_page_contents(soup)

    
    def scrape_pipeline(n=10,min_year=2007,max_year=2017):
        ''' For an inputted number n, returns text scrapped from n valid articles published between min_year and max_year'''
        assert type(n) == int
        assert n > 0
        remaining_articles = n
        raw_text = ''
        urls = Scraper.generate_random_url(n=None) 
        i = 0
        N = len(urls)
        
        while remaining_articles > 0 and i < N:
            
            # Grab article hyperlinks for arbitrary date
            new_articles = Scraper.scrape_articles(urls[i])
            if new_articles == []:
                print('Sleeping for ~3 seconds')
                sleep(random() + 3) # Experiment
            i += 1
            for article in new_articles:
                sleep(random()) # Avoid overloading the server
                article_text = Scraper.scrape_page(article)
                if article_text != '':
                    raw_text += ' ' + article_text 
                    remaining_articles -= 1

                if remaining_articles == 0:
                    break
        if i == N:
            print("Ran out of url's between years: " + min_year + '-' + max_year)
        
        
        return raw_text


         
