# -*- coding: utf-8 -*-

import os

from app.schemas import InvalidTokenResponse
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


async def authorized(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=True))) -> None:
    if auth.credentials != os.getenv('SEMANTIC_RSS_SEARCH_API_TOKEN'):
        raise HTTPException(status_code=403, detail=InvalidTokenResponse().detail)
