from bs4 import BeautifulSoup
from google import google
from selenium import *
import requests
import sys
import traceback
import re


# Now we need a function to handle the actual web scraping
# This method will make use of beautifulsoup, and should take in,
# just for starters, the title of the movie we want
def scrape(query):
    # get the rotten tomatoes page using google search
    
    # store the first page of search results
    num_page = 1
    search_results = google.search(query, num_page) # the list of results
        
    try:
        # get rotten tomato link 
        URL = search_results[0].link
        if URL == "https://www.rottentomatoes.com/":
            print("No movie specified!")
            sys.exit(0)
        elif "/search" in URL:
            print("Not allowed to crawl here!")
            sys.exit(0)
        response = requests.get(URL)
        # make sure request was valid
        if response.status_code != 200:
            print("Error retrieving the url specified by {}".format(URL))
            sys.exit(0)
    
        soup = BeautifulSoup(response.content, features="lxml")

        # now that we have the webpage, we need to get the information we need!
        # we need to get cast information, movie rating, and plot overview, and link to trailer
        
        # First get the title of the movie
        movie_title = soup.find("title").text
        print(movie_title)
        
        # now get synopsis
        movie_synopsis = soup.find(id="movieSynopsis")
        print("Synopsis:\n",movie_synopsis)

        # now get cast
        #movie_cast = soup.find_all("div", class_="cast-item media inlineBlock")
        cast = []
        for cast_item in soup.find_all("div", class_="cast-item media inlineBlock"):
            actor_name = cast_item.find("span").text.strip() 
            # now get role
            role = cast_item.find("span", class_="characters subtle smaller").text.strip()
            # remove new lines and possible carriage returns
            
            split_str = role.split()
            role = ""
            for w in split_str:
                if w != "":
                    role += (w+" ")
            role = role.strip()
            cast.append(actor_name+" "+role)
        
        # print the cast
        print("Cast:")
        for a in cast:
            print(a)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        sys.exit(0)


def main():
    # main code goes here
    '''
    this is how we will handle the system arguments
    print("Number of system arguments: {}".format(len(sys.argv)))

    # print all the arguments
    for a in sys.argv:
        print("{} ".format(a), end="")
    '''
    # make sure to pass title in as one word! This means you need to pass in the title
    # in quotes when passing in as system argument!
    try:
        title = sys.argv[1] + "rotten tomatoes"
    except Exception as e:
        print("No movie specified.")
        sys.exit(0)
    
    scrape(title)

# this will be the first thing to be run when the script opens
# it is only responsible for calling the main() function above it
# think about this as int main() in C or main in java
if __name__ == '__main__':
    main()
