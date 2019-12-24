# Movie Finder
Movie Finder is a Python script to help you find information on all the latest movies!

# Motivation
I love movies, but it can become rather tedious having to look up the ratings, reviews, cast, etc. Movie Finder eliminates all the hassle. You provide the movie you want to watch, whether it be new or old, and we'll go get all the information for you. The best part is, you don't even need to open your browser!

# Installation
To use this, simply download or clone the repository to whatever location you'd like!

# Usage
To search for a movie, all you need to do is pass in the title as a parameter of the program. Simply navigate within the project until you reach the
```bash
spiders
```
directory. Then run the following command:
```bash
python3 movies.py <movie_title or keyword>
```

If your movie contains more than one word, simply place quotes around it:
```bash
python3 movies.py "<movie_title or keyword>"
```

# Frameworks Used
+ Scrapy
+ BeautifulSoup

# TODO
+ add multiple movie request support [done]
+ Fix URL being None error [hopefully done]
+ add spell assumption, or some indication of "assuming you meant..."
+ Add ability to save results to external file; essentially a "save for later" option
