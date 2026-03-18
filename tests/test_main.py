# -*- coding: utf-8 -*-

import os

import app.main as main
import app.config as config
import tests.support.utils as utils

from fastapi.testclient import TestClient

client = TestClient(main.app)


def test_embed_not_authorized():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    response = client.post('/embed', json={'url': 'http://example.com/rss'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

    utils.reset_embeddings()


def test_embed_invalid_token():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    response = client.post('/embed', json={'url': 'http://example.com/rss'},
                           headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 403
    assert response.json() == {'detail': 'Invalid token'}

    utils.reset_embeddings()


def test_embed_invalid_feed():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    os.environ['SEMANTIC_RSS_SEARCH_API_TOKEN'] = 'valid_token'
    response = client.post('/embed', json={'url': 'http://example.com/rss'},
                           headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 500
    os.environ.pop('SEMANTIC_RSS_SEARCH_API_TOKEN')

    utils.reset_embeddings()


def test_embed_valid_feed():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    os.environ['SEMANTIC_RSS_SEARCH_API_TOKEN'] = 'valid_token'
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    response = client.post('/embed', json={'url': url}, headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 201
    data = response.json()
    assert 'entries' in data
    assert isinstance(data['entries'], int)
    assert data['entries'] > 0
    os.environ.pop('SEMANTIC_RSS_SEARCH_API_TOKEN')

    utils.reset_embeddings()


def test_search():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    os.environ['SEMANTIC_RSS_SEARCH_API_TOKEN'] = 'valid_token'
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    client.post('/embed', json={'url': url}, headers={'Authorization': 'Bearer valid_token'})

    response = client.post('/search', json={'query': 'When will Nasa travel to mars?', 'k': 2})
    assert response.status_code == 200
    data = response.json()
    assert 'results' in data
    assert isinstance(data['results'], list)
    assert len(data['results']) == 2
    assert data['results'][0]['title'] == 'The Engine That Does More'

    utils.reset_embeddings()


def test_search_accept_header_not_json():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    os.environ['SEMANTIC_RSS_SEARCH_API_TOKEN'] = 'valid_token'
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    client.post('/embed', json={'url': url}, headers={'Authorization': 'Bearer valid_token'})
    os.environ.pop('SEMANTIC_RSS_SEARCH_API_TOKEN')

    response = client.post('/search', json={'query': 'When will Nasa travel to mars?', 'k': 2},
                           headers={'Accept': 'text/plain'})
    assert response.status_code == 406
    assert response.json() == {'detail': 'Not acceptable'}

    utils.reset_embeddings()


def test_search_content_type_header_not_json():
    utils.reset_embeddings()
    main.embeddings = config.initialize_embeddings()

    os.environ['SEMANTIC_RSS_SEARCH_API_TOKEN'] = 'valid_token'
    url = 'https://sample-feeds.rowanmanning.com/examples/30493cdf1415a6cdc2f599c828d1b19c/feed.xml'
    client.post('/embed', json={'url': url}, headers={'Authorization': 'Bearer valid_token'})
    os.environ.pop('SEMANTIC_RSS_SEARCH_API_TOKEN')

    response = client.post('/search', json={'query': 'When will Nasa travel to mars?', 'k': 2},
                           headers={'Content-Type': 'text/plain'})
    assert response.status_code == 415
    assert response.json() == {'detail': 'Unsupported media type'}

    utils.reset_embeddings()
