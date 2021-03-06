# codinghorror https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fblog.codinghorror.com%2Frss%2F
# https://www.reddit.com/r/programming/comments/66678/ask_reddit_what_csprogramming_rss_feeds_should_i/

import urllib
import json


NEWS_SITES = {
    "codinghorror": "https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fblog.codinghorror.com%2Frss%2F",
    "lambda": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Flambda-the-ultimate.org%2Frss.xml",
    "bliki": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Fmartinfowler.com%2Fbliki%2Fbliki.atom",
    "joe": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Fwww.joelonsoftware.com%2Frss.xml",
    "feed": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Ffeeds.feedburner.com%2Ffreetechbooks",
    "orilly": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Fradar.oreilly.com%2Findex.rdf",
    "paul": "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Ffeeds.feedburner.com%2FPaulGrahamUnofficialRssFeed",
    "reddit_programming": "https://www.reddit.com/r/programming/.json"
}

DEFAULT_NEWS = "lambda"


def show_news(news_source):
    """return json response of news"""
    response = urllib.request.urlopen(NEWS_SITES[news_source])
    data = json.loads(response.read())
    return data
