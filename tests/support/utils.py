# -*- coding: utf-8 -*-

import os

from app.engine.embeddings import Embeddings


def reset_embeddings():
    if Embeddings._instance is None:
        return

    embeddings = Embeddings()
    embeddings.initialized = False
    dbname = embeddings.dbname
    if dbname and os.path.exists(dbname):
        os.remove(dbname)
    Embeddings._instance = None
