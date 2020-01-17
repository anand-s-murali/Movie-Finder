# Movie-Finder
Movie-Finder is a Python script to help you find information on all the latest movies!

# Motivation
I love movies, but looking up movies online, especially when I have multiple in mind, can get rather tedious. Instead of opening up multiple tabs for each movie or searching one up one by one, I wanted to be able to do them all in one go. With Movie-Finder, you can do exactly that! Simply type in the movies you're interested in, and we'll do the rest.

# Installation
To use this script, simply download or clone the repository to whatever location you'd like!

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
If the script is not working properly for you, it may because you need to install the dependencies listed under Frameworks/Libraries below. And keep in mind, this script requires [python3](https://www.python.org/downloads/).

# Storing Results
Through running this script, you will automatically generate a "watch_list" csv file (located in the same directory as the script). This file is only generated once (unless you delete it) and is used to store the results of your queries if you choose to store them.

# Third Party Frameworks/Libraries Needed
+ [Scrapy](https://scrapy.org/)
+ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
+ [googlesearch's API](https://python-googlesearch.readthedocs.io/en/latest/)

Any of these modules can be installed using pip as follows:
```bash
python3 -m pip install <module> --user
```

# TODO
+ Add multiple movie request support :white_check_mark:
+ Add ability to save results to external "watch list" :white_check_mark:
+ Allow threads to handle multiple inputs :white_check_mark:
+ Use pyQT5 for GUI interaction
+ Use database as backend storage as opposed to csv files
