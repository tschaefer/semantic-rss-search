# -*- coding: utf-8 -*-

import os
import pytest
import tests.support.utils as utils

from app.engine.embeddings import Embeddings
from app.engine.feed import Feed

dbname = os.getenv('SEMANTIC_RSS_SEARCH_DBNAME',
                   '/tmp/semantic_rss_search.db')


def test_embeddings_upsert_dimension_not_match():
    utils.reset_embeddings()

    embeddings = Embeddings(dbname=dbname, dimension=256)
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    feed = Feed(url)
    feed.parse()
    with pytest.raises(Exception, match='Expected 256 dimensions but received 768'):
        embeddings.upsert(feed)

    utils.reset_embeddings()


def test_embeddings_upsert_input_not_a_feed():
    utils.reset_embeddings()

    embeddings = Embeddings(dbname=dbname)
    with pytest.raises(AttributeError, match="'str' object has no attribute 'entries'"):
        embeddings.upsert('This is not a feed object')

    utils.reset_embeddings()


def test_embeddings_upsert_valid_feed():
    utils.reset_embeddings()

    embeddings = Embeddings(dbname=dbname)
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    feed = Feed(url)
    feed.parse()

    result = embeddings.upsert(feed)
    assert result is not None
    assert isinstance(result, int)
    assert result == len(feed.entries)

    with embeddings._Embeddings__connect_db() as db:
        cursor = db.execute('SELECT COUNT(*) FROM embeddings')
        count = cursor.fetchone()[0]
        assert count == len(feed.entries)

    utils.reset_embeddings()


def test_embeddings_search():
    utils.reset_embeddings()

    embeddings = Embeddings(dbname=dbname)
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    feed = Feed(url)
    feed.parse()
    embeddings.upsert(feed)

    query = 'When will Nasa travel to mars?'
    results = embeddings.search(query, k=2)

    assert results is not None
    assert isinstance(results, list)
    assert len(results) == 2

    key_fields = ['title', 'summary', 'published', 'link', 'distance', 'token']
    assert list(results[0].keys()) == key_fields

    utils.reset_embeddings()
