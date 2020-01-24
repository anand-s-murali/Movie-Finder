# Requires python3 

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from bs4 import BeautifulSoup
from googlesearch import search
import sys
import time
import traceback
import os
import csv
import threading

# global variable to store scraped results
scraped_data = [] 

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    synopsis = scrapy.Field()
    cast = scrapy.Field()
    rotten_rating = scrapy.Field()
    audience_rating = scrapy.Field()

class MovieSpider(scrapy.Spider):
    # name the spider and provide start url
    name = 'movie_module_spider'
    start_urls = []

    # define constructor; just needs the url from google
    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        
        # get the url parameter
        url = kwargs.get('url')
        # make sure url is found and is appropriate
        if not url:
            raise ValueError('Improper url or title given')
        
        # add the url to the start_url list
        self.start_urls.append(url)

    # performs the page parsing
    def parse(self, response):
        # define global scraped list
        global scraped_data
        # clear the list every time
        scraped_data = []

        # define other variables
        soup = BeautifulSoup(response.text, 'lxml')
        movie_info = MovieItem() # will be used to store scraped info
        
        # get the title and remove the ' - Rotten Tomato' portion
        title = soup.find('title').text
        index = title.find(' - Rotten Tomatoes')
        if index != -1:
            title = title[0:index]
        movie_info['title'] = title
        
        # get the synopsis
        synopsis = soup.find(id='movieSynopsis').text.strip()
        movie_info['synopsis'] = synopsis
    
        # get the cast
        cast = []
        for cast_item in soup.find_all('div', class_='cast-item media inlineBlock'):
            actor_name = cast_item.find('span').text.strip()
            # now get the role
            role = cast_item.find('span', class_='characters subtle smaller').text.strip()

            # remove the new lines and format string
            split_str = role.split()
            role = ''
            for w in split_str:
                if w != '':
                    role += (w+' ')
            # get rid of last space
            role = role.strip()
            # add the actor and the cast
            cast.append(actor_name+' '+role)
        
        movie_info['cast'] = cast

        # get the rotten tomato score and audience score by iterating over specific spans
        ratings = []
        for r in soup.find_all('span', class_='mop-ratings-wrap__percentage'):
            ratings.append(r.get_text().strip())
       
        movie_info['rotten_rating'] = ratings[0]
        movie_info['audience_rating'] = ratings[1]
       
        # add movie info to list if it is not already there
        for mv in scraped_data:
            if mv['title'] == movie_info['title']:
                return
        
        # only add the movie if we haven't seen it
        scraped_data.append(movie_info)

def scrape(query, process):
    # google search the query
    search_results = search(query, tld='com', lang='en', safe='on', num=10, start=0, stop=5, pause=2.0, country='us')

    try:
        # get the rotten tomato link; will contain /m/ in the url
        URL = ''
        for res in search_results:
            if 'https://www.rottentomatoes.com/m/' in res:
                URL = res
                break

        # handle possible errors with the URL
        if URL is None:
            # print(search_results)
            raise ValueError('URL was none. Quitting.')
        elif URL == 'https://www.rottentomatoes.com/':
            raise ValueError('No movie specified. Please enhance your search query.')

        # initiate the crawling
        process.crawl(MovieSpider, url=URL)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)


def handle(query):
    # try:
    process = CrawlerProcess(settings=get_project_settings())
    # scrape the data
    scrape(query+' rotten tomatoes', process)
    process.start()
    
    global scraped_data
    movie = scraped_data[0]

    '''
    # output results
    print('{}:'.format(movie['title']))
    print('{}\n'.format(movie['synopsis']))
    print('Cast: {}\n'.format(', '.join(movie['cast'])))
    print('Rotten tomato score: {}, Audience score: {}\n'.format(movie['rotten_rating'], movie['audience_rating']))
    '''

    # return the movie
    return movie

    #except Exception as e:
    # print(e)
    # print('Error getting title. Please improve your search query.')
