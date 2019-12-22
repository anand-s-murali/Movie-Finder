import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import sys
import time
from google import google
#from bs4 import BeautifulSoup
#import requests

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    synopsis = scrapy.Field()
    cast = scrapy.Field()
    rating = scrapy.Field()

class MovieSpider(scrapy.Spider):
    # name the spider and provide start url
    name = "movie_spider"
    start_urls = []

    # define constructor; just needs the url from google
    def __init__(self, *args, **kwargs):
        # some funky business
        super(MovieSpider, self).__init__(*args, **kwargs)
        
        # get the url parameter
        url = kwargs.get("url")
        # make sure url is found and is appropriate
        if not url:
            print(url)
            raise ValueError("Improper url given")
        if not isinstance(url, str):
            print(type(url))
            raise ValueError("url passed is not a string!")
        # add the url to the start_url list
        self.start_urls.append(url)

    # perform the scraping over the given links (just one for now)
    def start_requests(self):
        for url in self.start_urls:
            # get splash request
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')
    
    # performs the page parsing
    def parse(self, response):
        print(response.css)

def scrape(query):
    # get the rotten tomatoes page using google search and store the first page of search results
    num_page = 1
    search_results = google.search(query, num_page)
    # we only want to try three times...
    flag = 1
    while(len(search_results) != 10 and flag < 3):
        # sleep for a little bit so not to get banned
        print("sleeping...")
        time.sleep(2)
        search_results = google.search(query,num_page)
        flag += 1

    # handle flag error
    if flag == 3:
        raise ValueError("Unable to get page. Consider rewording your search query.")

    try:
        # get rotten tomato link
        URL = search_results[0].link
        if URL == "https://www.rottentomatoes.com/":
            print("No movie specified!")
            sys.exit(1)
        elif "/search" in URL:
            print("Not allowed to crawl here!")
            sys.exit(1)

        # start the scraping!
        process = CrawlerProcess(settings=get_project_settings())
        process.crawl(MovieSpider, url=URL)
        process.start()        
    except IndexError:
        print(search_results)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

# main method
def main():
    # main code goes here
    # make sure to pass title in as one word! This means you need to pass in the title
    # in quotes if the title is multiple words when passing in as system argument!
    try:
        movie_query = sys.argv[1] + "rotten tomatoes"
    except Exception as e:
        print("No movie specified.")
        sys.exit(0)
    
    scrape(movie_query)

# this will be the first thing to be run when the script opens
# it is only responsible for calling the main() function above it
# think about this as int main() in C or main in java
if __name__ == "__main__":
    main()
