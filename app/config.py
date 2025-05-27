# -*- coding: utf-8 -*-

import logging
import os

from app.engine.embeddings import Embeddings


description = """
Index and search RSS feeds using semantic search techniques.
This API provides endpoints to embed RSS feed entries into a vector database
and search them based on semantic similarity.

### Index RSS Feeds

Index RSS feeds by posting their URLs to the `/embed` endpoint. This will
parse the feed entries and store title, summary, published date, link, and
vector embeddings in the database. The vector embeddings are based on the
content of the title and summary.

The endpoint requires authorization with a bearer token, which must be set
as an environment variable `SEMANTIC_RSS_SEARCH_API_TOKEN`.

### Search RSS Feeds

Search indexed RSS feeds by posting a query to the `/search` endpoint.
The search will return the top `k` entries that match the query based on
semantic similarity. The results include the title, summary, published date,
link, distance from the query vector, and the number of tokens of the indexed
content.
"""


def create_info():
    return {
        'docs_url': None,
        'title': 'Semantic RSS Search API',
        'summary': 'A Solid Semantic Search for RSS Feeds 🗞️.',
        'description': description,
        'version': '0.1.0',
        'license_info': {
            'name': 'MIT License',
            'url': 'https://github.com/tschaefer/semantic-rss-search?tab=MIT-1-ov-file',
        },
    }


def initialize_embeddings():
    logger = logging.getLogger('uvicorn.error')

    dbname = os.getenv('SEMANTIC_RSS_SEARCH_DB', 'db/semantic_rss_search.db')
    embeddings = Embeddings(dbname=dbname)
    logger.info('Initialized embeddings model and database.')

    return embeddings


def verify_environment():
    if not os.getenv("SEMANTIC_RSS_SEARCH_API_TOKEN", None):
        raise ValueError("Environment variable SEMANTIC_RSS_SEARCH_API_TOKEN is not set.")
