# -*- coding: utf-8 -*-

import nltk
import numpy as np
import sqlite3
import sqlite_vec

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


class Embeddings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Embeddings, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbname='db/semantic_rss_search.db', dimension=768,
                 model='BAAI/bge-base-en-v1.5'):
        if hasattr(self, 'initialized'):
            return

        self.dbname = dbname
        self.dimension = dimension
        self.model = model

        self.transformer = SentenceTransformer(self.model)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)

        self.__init_db()
        self.initialized = True

    def __connect_db(self):
        db = sqlite3.connect(self.dbname, check_same_thread=False)
        db.execute('PRAGMA journal_mode=WAL;')
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        return db

    def __vectorization(self, sentences):
        return self.transformer.encode(' '.join(sentences)).astype(np.float32)

    def __extract_keywords(self, query):
        tokens = nltk.word_tokenize(query)
        tagged = nltk.pos_tag(tokens)
        keep_tags = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS'}
        keywords = [word for word, tag in tagged if tag in keep_tags]
        return keywords if keywords else tokens

    def __init_db(self):
        with self.__connect_db() as db:
            db.execute(f'''
                CREATE VIRTUAL TABLE IF NOT EXISTS embeddings
                USING vec0(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    summary TEXT,
                    published FLOAT,
                    link TEXT,
                    token INTEGER,
                    vector float[{self.dimension}]
                );
            ''')
            db.commit()

    def upsert(self, feed):
        with self.__connect_db() as db:
            for entry in feed.entries:
                tokens = self.tokenizer.encode(' '.join(entry.sentences), add_special_tokens=True)
                token_count = len(tokens)
                vector = self.__vectorization(entry.sentences)

                result = db.execute('SELECT id FROM embeddings WHERE link = ?', (entry.link,)).fetchone()

                if result:
                    db.execute('''
                        UPDATE embeddings
                        SET title = ?, summary = ?, published = ?, token = ?, vector = ?
                        WHERE id = ?;
                    ''', (entry.title, entry.summary, entry.published, token_count, vector, result[0]))
                else:
                    db.execute('''
                        INSERT INTO embeddings (title, summary, published, link, token, vector)
                        VALUES (?, ?, ?, ?, ?, ?);
                    ''', (entry.title, entry.summary, entry.published, entry.link, token_count, vector))
            db.commit()

        return len(feed.entries)

    def search(self, query, k=5):
        keywords = self.__extract_keywords(query)
        vector = self.__vectorization(keywords)

        with self.__connect_db() as db:
            cursor = db.execute('''
                SELECT title, summary, published, link, distance, token
                FROM embeddings
                WHERE vector MATCH ? AND k = ?
                ORDER BY distance ASC;
            ''', (vector, k))

            results = cursor.fetchall()

        return [
            {
                "title": r[0],
                "summary": r[1],
                "published": r[2],
                "link": r[3],
                "distance": r[4],
                "token": r[5],
            }
            for r in results
        ] if results else []
