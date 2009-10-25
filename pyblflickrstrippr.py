#!/bin/env python
"""
A Pyblosxom plugin to fetch photos from a Flickr RSS feed.

Configuration:
  The following variables must be set in your config.py
  - "flickrfeed" the url to a flickr rss feed

  Optional
  - "num_flickr_photos" to override the default of 6.

Use:
  refer to $tweets in your templates to generate an
  html unordered list <ul>

CSS Hooks:
  ul class  blosxomFlickr
  li class  blosxomFlickrPhoto
"""

import feedparser
import re

__author__ = "Devon Meunier <devon.meunier@myopicvoid.org>"
__version__ = "0.1"
__url__ = "http://myopicvoid.org/"
__description__ = "Display flickr thumbnails from an rss feed."

def verify_installation(request):
    config = request.getConfiguration()
    if config.has_key("flickrfeed"):
      print "    Flickr Feed URL: " + config["flickrfeed"]
      return 1
    return 0

class PyblFlickrStrippr:
  def __init__(self, request):
    self._request = request
    self._config = request.getConfiguration()
    self._photos = None

  def __str__(self):
    if self._photos is None:
      self._photos = self.generatePhotos()
    return self._photos

  def generatePhotos(self):
    feedurl = self._config["flickrfeed"]
    feed = feedparser.parse(feedurl)
    num_photos = 5
    if self._config.has_key("num_flickr_photos"):
      num_photos = self._config["num_flickr_photos"]

    res = "<ul class='blosxomFlickr'>"
    for i in range(0, num_photos):
      s = str(feed.entries[i].description)
      search = re.search("<a.*?<img.*?>.*?</a>", s)
      res += "<li class='blosxomFlickrPhoto'>" + search.group(0) + "</li>"
    res += "</ul>"

    return res.encode('utf-8')

def cb_prepare(args):
  request = args["request"]
  config = request.getConfiguration()
  data = request.getData()
  data["flickrphotos"] = PyblFlickrStrippr(request)
