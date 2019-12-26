# Movie Finder
Movie Finder is a Python script to help you find information on all the latest movies!

# Motivation
I love movies, but it can become rather tedious having to look up the ratings, reviews, cast, etc. Movie Finder eliminates all the hassle. You provide the movie you want to watch, whether it be new or old, and we'll go get all the information for you. The best part is, you don't even need to open your browser!

# Installation
To use this, simply download or clone the repository to whatever location you'd like!

# Usage
To search for a movie, simply navigate within the project directory until you are within the spiders directory: 
```bash
cd movie/movie/spiders/
```
Then run the following command:
```bash
python3 movies.py <title>
```
If your movie contains more than one word, simply place quotes around it:
```bash
python3 movies.py "<movie title>"
```
If you'd like to request more than one movie, just separate each title with a space and follow the guidelines above:
```bash
python3 movies.py <title1> <title2> ... <title n>
```

# Storing Results
Through running this script, you will automatically generate a "watch_list" csv file (located in the same directory as the script). This file is only generated once, unless you delete it, and is used to store the results of your queries if you choose to store them.

# Frameworks/Libraries Used
+ [Scrapy](https://scrapy.org/)
+ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
+ [Google Search API](https://github.com/abenassi/Google-Search-API)

# TODO
+ add multiple movie request support :white_check_mark:
+ Fix URL being None error [hopefully fixed]
+ Add ability to save results to external file; essentially a "save for later" option :white_check_mark:
+ add spell assumption, or some indication of "assuming you meant..."
