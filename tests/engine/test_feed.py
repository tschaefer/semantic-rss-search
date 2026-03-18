# -*- coding: utf-8 -*-

import pytest

from app.engine.feed import Feed


def test_feed_initialization():
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    feed = Feed(url)
    assert feed.url == url
    assert feed.entries is None


def test_feed_parse_invalid_url():
    invalid_url = 'https://local.host:8000/invalid_feed.xml'
    feed = Feed(invalid_url)
    with pytest.raises(Exception, match='Unable to parse the feed:'):
        feed.parse()


def test_feed_parse_invalid_feed():
    invalid_feed_url = 'https://example.com/'
    feed = Feed(invalid_feed_url)
    with pytest.raises(Exception, match='Unable to parse the feed:'):
        feed.parse()


def test_feed():
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    feed = Feed(url)
    feed.parse()

    assert len(feed.entries) > 0
    for entry in feed.entries:
        assert hasattr(entry, 'title')
        assert hasattr(entry, 'summary')
        assert hasattr(entry, 'published')
        assert hasattr(entry, 'link')
