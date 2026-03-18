# -*- coding: utf-8 -*-

from fastapi import Request
from fastapi.responses import JSONResponse
from app.schemas import NotAcceptableResponse, UnsupportedMediaTypeResponse

API_ROUTES = [
    "/search",
    "/embed",
]


async def accept_header(request: Request, call_next):
    if request.url.path not in API_ROUTES:
        return await call_next(request)

    allowed_accepts = ["application/json", "*/*"]
    accept = request.headers.get("Accept")
    if accept is not None and accept not in allowed_accepts:
        return JSONResponse(status_code=406, content={'detail': NotAcceptableResponse().detail})
    return await call_next(request)


async def content_type_header(request: Request, call_next):
    if request.url.path not in API_ROUTES:
        return await call_next(request)

    allowed_content_types = ["application/json"]
    content_type = request.headers.get("Content-Type")
    if content_type is None or content_type not in allowed_content_types:
        return JSONResponse(status_code=415, content={'detail': UnsupportedMediaTypeResponse().detail})
    return await call_next(request)
