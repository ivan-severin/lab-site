# Laboratiry site for IOP Ukraine
Simple site for our laboratory written in Flask. 

Based on [//charlesleifer's](http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)
tutorial with few changes.

### Installation

#### Virtual enviroment:
```sh
$ virtualenv --python=python2 --prompt="(Flask)" env 
$ source env/bin/activate
```
#### Dependencies:

* [Flask](http://flask.pocoo.org/), a lightweight web framework.
* [Peewee](http://docs.peewee-orm.com/en/latest/), for storing entries in the database and executing queries.
* [pygments](http://pygments.org/), syntax highlighting with support for a ton of different languages.
* [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), formatting for our entries.
* [micawber](http://charlesleifer.com/blog/micawber-a-python-library-for-extracting-rich-content-from-urls/), for converting URLs into rich content objects. For example if you wanted to embed a YouTube video, just place the URL to the video in your post and a video player will automagically appear in its place.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), required by micawber for parsing HTML.

Installation those dependencies with pip:

```sh
$ pip install -r Requirements.txt
```

### Starting local server
```sh
$ python app.py
```
