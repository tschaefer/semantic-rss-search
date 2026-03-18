FROM python:3.13-slim-bookworm

WORKDIR /app

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir setuptools wheel && \
    pip install --no-cache-dir bs4 "fastapi[standard]" feedparser numpy && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir nltk sentence_transformers sqlite_vec transformers && \
    python -W ignore -m nltk.downloader -d /app/venv/nltk_data punkt_tab averaged_perceptron_tagger_eng

COPY . .

RUN addgroup --system app && \
    adduser --system --uid 1000 --ingroup app app && \
    chown -R app:app /app

USER app

ENV NLTK_DATA=/app/venv/nltk_data \
    HF_HOME=/app/models

LABEL org.opencontainers.image.source=https://github.com/tschaefer/semantic-rss-search \
      org.opencontainers.image.description="A Solid Semantic Search for RSS Feeds." \
      org.opencontainers.image.licenses=MIT

VOLUME ["/app/db", "/app/models"]

EXPOSE 8000

CMD ["venv/bin/python", "run.py"]
