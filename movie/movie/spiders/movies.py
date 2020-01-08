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
    name = "movie_spider"
    start_urls = []

    # define constructor; just needs the url from google
    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        
        # get the url parameter
        url = kwargs.get("url")
        # make sure url is found and is appropriate
        if not url:
            raise ValueError("Improper url or title given")
        
        # add the url to the start_url list
        self.start_urls.append(url)

    # performs the page parsing
    def parse(self, response):
        # define global scraped list
        global scraped_data

        # define other variables
        soup = BeautifulSoup(response.text, 'lxml')
        movie_info = MovieItem() # will be used to store scraped info
        
        # get the title and remove the " - Rotten Tomato" portion
        title = soup.find("title").text
        index = title.find(" - Rotten Tomatoes")
        if index != -1:
            title = title[0:index]
        movie_info["title"] = title
        
        # get the synopsis
        synopsis = soup.find(id="movieSynopsis").text.strip()
        movie_info["synopsis"] = synopsis
    
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
        
        movie_info["cast"] = cast

        # get the rotten tomato score and audience score by iterating over specific spans
        ratings = []
        for r in soup.find_all("span", class_="mop-ratings-wrap__percentage"):
            ratings.append(r.get_text().strip())
       
        movie_info["rotten_rating"] = ratings[0]
        movie_info["audience_rating"] = ratings[1]
       
        # add movie info to list if it is not already there
        for mv in scraped_data:
            if mv["title"] == movie_info["title"]:
                return
        
        # only add the movie if we haven't seen it
        scraped_data.append(movie_info)
        
def scrape(query, process):
    # google search the query
    search_results = search(query, tld="com", lang="en", safe="on", num=10, start=0, stop=5, pause=2.0, country="us")

    try:
        # get the rotten tomato link; will contain /m/ in the url
        URL = ""
        for res in search_results:
            if "https://www.rottentomatoes.com/m/" in res:
                URL = res
                break

        # handle possible errors with the URL
        if URL is None:
            # print(search_results)
            raise ValueError("URL was none. Quitting.")
        elif URL == "https://www.rottentomatoes.com/":
            raise ValueError("No movie specified. Please enhance your search query.")

        # initiate the crawling
        process.crawl(MovieSpider, url=URL)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)

# main code goes here
def main():
    # print statement just to separate command execution from output
    print()

    ''' START SCRAPING AND THREADING'''
    # create the crawler process; this will be responsible for scraping all the data
    process = CrawlerProcess(settings=get_project_settings())
    
    # create a list for all the threads
    threads = []

    # iterate over all movies presented (from system arguments)
    for i in range(1, len(sys.argv)):
        # update the query 
        query = sys.argv[i] + " rotten tomatoes"
        
        # create the thread, append the thread to the list, and start it
        thread = threading.Thread(target=scrape, args=(query,process,))
        threads.append(thread)
        thread.start()
    
    # join all the threads - make main thread wait for all to finish 
    # this needs to come *before* process.start()
    for t in threads:
        t.join()

    # start crawler 
    process.start()
    ''' END SCRAPING AND THREADING '''

    
    ''' START OUTPUT AND SAVING '''
    # open our watch list file
    path = "./watch_list.csv"
    flag = os.path.isfile(path)
    watch_file = open(path, "a+")
    
    # check if this is the first time we are opening file
    # if it is, just write the main header
    watch_writer = csv.writer(watch_file, delimiter=",", quotechar="'")
    if not flag:
        # define the columns of the file
        watch_writer.writerow(["Title","Synopsis","Cast","Scores"])

    # iterate over each movie and ask if we want to print/save results 
    for movie in scraped_data:
        # ask if we want to print this movie to console
        while True:
            val = input("Would you like to print {} to console? [y/n] ".format(movie["title"]))
            if val == "y":
                print("{}:".format(movie["title"]))
                print("{}\n".format(movie["synopsis"]))
                print("Cast: {}\n".format(", ".join(movie["cast"])))
                print("Rotten tomato score: {}, Audience score: {}\n".format(movie["rotten_rating"], movie["audience_rating"]))
                
                break
            elif val == "n":
                break
            else:
                print("Input not understood.")
                    
        # ask if we want to save to file 
        while True:
            val = input("Would you like to save this title to your watch list? [y/n] ")
            if val == "y":
                watch_writer.writerow(["{}".format(movie["title"]), "{}".format(movie["synopsis"].replace(",","").replace("'","")), "{}".format(" | ".join(movie["cast"])).replace("'",""), "Rotten rating: {} | Audience Rating: {}".format(movie["rotten_rating"], movie["audience_rating"])]) 
                print("Title saved successfully!")
        
                break
            elif val == "n":
                break
            else:
                print("Input not understood.")
                    
        print("----------------------------------------------------------\n")

    # close file 
    watch_file.close()
    ''' END OUTPUT AND SAVING '''

if __name__ == "__main__":
    main()
