# -*- coding: utf-8 -*-

from pydantic import BaseModel, AnyHttpUrl


class SearchRequest(BaseModel):
    query: str
    k: int = 5


class SearchEntryResponse(BaseModel):
    title: str
    summary: str
    published: float
    link: AnyHttpUrl
    distance: float
    token: int


class SearchResponse(BaseModel):
    query: str
    k: int
    results: list[SearchEntryResponse]


class EmbedRequest(BaseModel):
    url: AnyHttpUrl


class EmbedResponse(BaseModel):
    entries: int


class NotAuthenticatedResponse(BaseModel):
    detail: str = "Not authenticated"


class InvalidTokenResponse(BaseModel):
    detail: str = "Invalid token"


def authorization_responses():
    return {
        401: dict(model=NotAuthenticatedResponse),
        403: dict(model=InvalidTokenResponse)
    }
