# Movie-Finder
Movie Finder is a Python script to help you find information on all the latest movies!

# Motivation
I love movies, but it looking up movies over the internet, especially when I have a few in mid. Movie-Finder now eliminates all the hassle; you provide the movie you want to watch, whether they be new or old, and we'll go get all the information for you. Moreover, per your instructions, we'll save your movies to an external "watch list" file for you to go back to later if you ever forget!

# Installation
This script requires [python3](https://www.python.org/downloads/)

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
If the script is not working properly for you, it may because you need to install the dependencies listed under Frameworks/Libraries below.

# Storing Results
Through running this script, you will automatically generate a "watch_list" csv file (located in the same directory as the script). This file is only generated once (unless you delete it) and is used to store the results of your queries if you choose to store them.

# Frameworks/Libraries Used
+ [Scrapy](https://scrapy.org/)
+ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
+ [Google Search API](https://github.com/abenassi/Google-Search-API)

# TODO
+ add multiple movie request support :white_check_mark:
+ Fix URL being None error :white_check_mark:
+ Add ability to save results to external file; essentially a "save for later" option :white_check_mark:
+ Should probably be using threads to handle multiple inputs...
