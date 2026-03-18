# -*- coding: utf-8 -*-

import calendar
import collections
import feedparser
import nltk
import time

from bs4 import BeautifulSoup


FeedEntry = collections.namedtuple('FeedEntry', ['title', 'summary', 'published', 'link', 'sentences'])


class Feed:
    def __init__(self, url):
        self.url = url
        self.entries = None

    def parse(self):
        feed = feedparser.parse(self.url)
        if feed.bozo:
            message = 'Unable to parse the feed: {}'.format(feed.bozo_exception)
            raise Exception(message)

        if 'entries' not in feed or not feed.entries:
            self.entries = []
            return

        self.__build_entries(feed)

    def __build_entries(self, feed):
        entries = []
        for entry in feed.entries:
            title = entry.get('title', 'No title').replace('\n', ' ').strip()
            summary = entry.get('summary', 'No summary').replace('\n', ' ').strip()

            published = time.mktime(entry['published_parsed']) if 'published_parsed' in entry else calendar.timegm(time.gmtime())
            link = entry.get('link', None)

            sentences = nltk.tokenize.sent_tokenize(self.__strip_html(title) + ' ' +
                                                    self.__strip_html(summary))
            entries.append(self.__create_feed_entry(title, summary, published, link, sentences))

        self.entries = entries

    def __strip_html(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()

    def __create_feed_entry(self, title, summary, published, link, sentences):
        return FeedEntry(
            title,
            summary,
            published,
            link,
            sentences
        )
