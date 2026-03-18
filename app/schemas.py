# -*- coding: utf-8 -*-

from pydantic import BaseModel, AnyHttpUrl, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    k: int = Field(default=5, ge=1, le=100)


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


class NotAcceptableResponse(BaseModel):
    detail: str = "Not acceptable"


class UnsupportedMediaTypeResponse(BaseModel):
    detail: str = "Unsupported media type"


def authorization_responses():
    return {
        401: dict(model=NotAuthenticatedResponse),
        403: dict(model=InvalidTokenResponse)
    }


def header_responses():
    return {
        406: dict(model=NotAcceptableResponse),
        415: dict(model=UnsupportedMediaTypeResponse)
    }
