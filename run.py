# -*- coding: utf-8 -*-

import os
import uvicorn
import app.config as config

if __name__ == "__main__":
    config.verify_environment()

    host = os.getenv("SEMANTIC_RSS_SEARCH_HOST", "0.0.0.0")
    port = int(os.getenv("SEMANTIC_RSS_SEARCH_PORT", 8000))

    uvicorn.run("app.main:app", headers=[("server", "search-feeds")], host=host, port=port)
