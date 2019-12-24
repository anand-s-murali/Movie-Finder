import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import sys
import time
from google import google
from bs4 import BeautifulSoup
import traceback


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    synopsis = scrapy.Field()
    cast = scrapy.Field()
    rotten_rating = scrapy.Field()
    audience_rating = scrapy.Field()


# global variable to store scraped results
# not good practice, but okay for what we are doing
# scraped_data = dict()
scraped_data = list()

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
            raise ValueError("url passed is not a string!")
        # add the url to the start_url list
        self.start_urls.append(url)

    # performs the page parsing
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        movie_info = MovieItem()
        
        # get the title
        title = soup.find("title").text
        movie_info["title"] = title 
        # scraped_data["title"] = title

        # get the synopsis
        synopsis = soup.find(id="movieSynopsis").text.strip()
        movie_info["synopsis"] = synopsis
        # scraped_data["synopsis"] = synopsis

        # get the cast
        cast = []
        for cast_item in soup.find_all("div", class_="cast-item media inlineBlock"):
            actor_name = cast_item.find("span").text.strip()
            # now get the role
            role = cast_item.find("span", class_="characters subtle smaller").text.strip()

            # remove the new lines and format string
            split_str = role.split()
            role = ""
            for w in split_str:
                if w != "":
                    role += (w+" ")
            # get rid of last space
            role = role.strip()
            # add the actor and the cast
            cast.append(actor_name+" "+role)
        
        # set the cast
        movie_info["cast"] = cast
        # scraped_data["cast"] = cast

        # get the rotten tomato score and audience score by iterating over specific spans
        # iterate over each span
        ratings = []
        for r in soup.find_all("span", class_="mop-ratings-wrap__percentage"):
            ratings.append(r.get_text().strip())

        movie_info["rotten_rating"] = ratings[0]
        movie_info["audience_rating"] = ratings[1]
        # scraped_data["rotten_rating"] = ratings[0]
        # scraped_data["audience_rating"] = ratings[1]
       
        '''
        # now we just need to print our results!
        print("{}\n".format(scraped_data["title"]))
        print("{}\n".format(scraped_data["synopsis"]))
        print("Cast: {}\n".format(", ".join(scraped_data["cast"])))
        print("Rotten tomato score: {}, Audience score: {}".format(scraped_data["rotten_rating"], scraped_data["audience_rating"]))
        '''
    
        # add movie info to list if it is not already there
        for mv in scraped_data:
            if mv["title"] == movie_info["title"]:
                return
        scraped_data.append(movie_info)
        
        # yield 
        # yield movie_info
        
def scrape(query, process):
    # get the rotten tomatoes page using google search and store the first page of search results
    num_page = 1
    search_results = google.search(query, num_page)
    # we only want to try 5 times...
    flag = 1
    while(len(search_results) == 0 and flag < 5):
        # sleep for a little bit so not to get banned
        # print("sleeping...")
        time.sleep(2)
        search_results = google.search(query,num_page)
        flag += 1

    # handle flag error
    if flag == 5:
        raise ValueError("Unable to get page. Consider rewording your search query.")
    
    try:
        # get rotten tomato link
        URL = search_results[0].link
        if URL is None:
            print(search_results)
            print("attempts: {}".format(flag))
            raise ValueError("URL was none. Quitting.")
        elif URL == "https://www.rottentomatoes.com/":
            print("No movie specified!")
            sys.exit(1)
        elif "/search" in URL:
            print("Not allowed to crawl here!")
            sys.exit(1)

        
        # start the scraping!
        # process = CrawlerProcess(settings=get_project_settings())
        process.crawl(MovieSpider, url=URL)
        '''
        # process.start()
        # now we just need to print our results!
                '''
    except IndexError:
        print(search_results)
        sys.exit(1)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        sys.exit(1)

# main method
def main():
    # main code goes here
    # make sure to pass title in as one word! This means you need to pass in the title
    # in quotes if the title is multiple words when passing in as system argument!
    '''
    try:
        movie_query = sys.argv[1] + "rotten tomatoes"
    except Exception as e:
        print("No movie specified.")
        sys.exit(0)
    
    scrape(movie_query)
    '''
    # create the crawler process
    process = CrawlerProcess(settings=get_project_settings())
    # iterate over all movies presented
    for i in range(1, len(sys.argv)):
        query = sys.argv[i] + " rotten tomatoes"
        scrape(query, process)

    # start the process after crawling everything!
    process.start()

    # print results
    for movie in scraped_data:
        print("{}:".format(movie["title"]))
        print("{}\n".format(movie["synopsis"]))
        print("Cast: {}\n".format(", ".join(movie["cast"])))
        print("Rotten tomato score: {}, Audience score: {}\n".format(movie["rotten_rating"], movie["audience_rating"]))
        print("----------------------------------------------------------")
    

# this will be the first thing to be run when the script opens
# it is only responsible for calling the main() function above it
# think about this as int main() in C or main in java
if __name__ == "__main__":
    main()
