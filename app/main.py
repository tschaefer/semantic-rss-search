# -*- coding: utf-8 -*-

import app.schemas as schemas
import app.security as security
import app.config as config
import app.middleware as middleware

from app.engine.feed import Feed
from fastapi import Depends, FastAPI, HTTPException


app = FastAPI(**config.create_info())
embeddings = config.initialize_embeddings()

app.middleware("http")(middleware.accept_header)
app.middleware("http")(middleware.content_type_header)


@app.post('/search', response_model=schemas.SearchResponse,
          responses=schemas.header_responses())
async def search(search: schemas.SearchRequest):
    try:
        query = search.query.strip()
        k = search.k

        results = embeddings.search(query, k=k)

        return {'results': results, 'query': query, 'k': k}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/embed', response_model=schemas.EmbedResponse,
          responses={**schemas.authorization_responses(), **schemas.header_responses()}, status_code=201)
async def embed(embed: schemas.EmbedRequest, _: None = Depends(security.authorized)):
    try:
        url = str(embed.url)

        feed = Feed(url)
        feed.parse()
        entries = embeddings.upsert(feed)

        return {'entries': entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
