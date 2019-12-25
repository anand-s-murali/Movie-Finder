import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import sys
import time
from google import google
from bs4 import BeautifulSoup
import traceback
import os
import csv

# global variable to store scraped results
# not good practice, but okay for what we are doing
scraped_data = list()

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
        # some funky business
        super(MovieSpider, self).__init__(*args, **kwargs)
        
        # get the url parameter
        url = kwargs.get("url")
        # make sure url is found and is appropriate
        if not url:
            # print(url)
            raise ValueError("Improper url or title given")
        if not isinstance(url, str): 
            raise ValueError("url passed is not a string!")
        # add the url to the start_url list
        self.start_urls.append(url)
        # set the title

    # performs the page parsing
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        movie_info = MovieItem()
        
        # get the title
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
        
        # set the cast
        movie_info["cast"] = cast

        # get the rotten tomato score and audience score by iterating over specific spans
        # iterate over each span
        ratings = []
        for r in soup.find_all("span", class_="mop-ratings-wrap__percentage"):
            ratings.append(r.get_text().strip())

        movie_info["rotten_rating"] = ratings[0]
        movie_info["audience_rating"] = ratings[1]
       
        # add movie info to list if it is not already there
        for mv in scraped_data:
            if mv["title"] == movie_info["title"]:
                return
        # add the movie if we haven't seen it
        scraped_data.append(movie_info)
        
def scrape(query, process):
    # get the rotten tomatoes page using google search and store the first page of search results
    num_page = 1
    search_results = google.search(query, num_page)
    # we only want to try 5 times...
    flag = 1
    while((len(search_results) == 0 or search_results is None) and flag < 5):
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
        # initiate the crawling
        process.crawl(MovieSpider, url=URL)
    except IndexError:
        print(search_results)
        sys.exit(1)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        sys.exit(1)

# main code goes here
def main():
    # just to make output nicer!
    print("\n")
    # open our watch list file
    path = "./watch_list.csv"
    flag = os.path.isfile(path)
    watch_file = open(path, "a+")
    
    # check if this is the first time we are opening file
    # if it is, just write the main header
    watch_writer = csv.writer(watch_file, delimiter=",", quotechar="'")
    if not flag:
        # write the headers
        watch_writer.writerow(["Title","Synopsis","Cast","Scores"])

    # create the crawler process
    process = CrawlerProcess(settings=get_project_settings())
    # iterate over all movies presented (from system arguments)
    for i in range(1, len(sys.argv)):
        query = sys.argv[i] + " rotten tomatoes"
        scrape(query, process)

    # start the process after crawling everything!
    process.start()
    
    # Add ability to save data to file
    # iterate over each movie and see if we would like to output and save results
    for movie in scraped_data:
        # first ask if we want to print this movie to console
        flag = False
        while True:
            val = input("Would you like to print {} to console? [y/n] ".format(movie["title"]))
            if val == "y":
                flag = True
                # just to add some buffer space and make output nicer!
                print()
                break
            elif val == "n":
                break
            else:
                print("Input not understood.")
        
        # print if flag
        if flag:
            print("{}:".format(movie["title"]))
            print("{}\n".format(movie["synopsis"]))
            print("Cast: {}\n".format(", ".join(movie["cast"])))
            print("Rotten tomato score: {}, Audience score: {}\n".format(movie["rotten_rating"], movie["audience_rating"]))
        
        # now check about saving to file
        flag = False
        while True:
            val = input("Would you like to save this title to your watch list? [y/n] ")
            if val == "y":
                flag = True
                # just to add some buffer space and make output nicer!
                print()
                break
            elif val == "n":
                break
            else:
                print("Input not understood.")

        # save to file if flag
        if flag:
            # open file and save to it
            watch_writer.writerow(["{}".format(movie["title"]), "{}".format(movie["synopsis"].replace(",","")), "{}".format(" | ".join(movie["cast"])), "Rotten rating: {} | Audience Rating: {}".format(movie["rotten_rating"], movie["audience_rating"])]) 
            print("Saved successfully")
        
        print("----------------------------------------------------------\n")

    # close the file at the end!
    watch_file.close()

if __name__ == "__main__":
    main()
