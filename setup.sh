#!/bin/bash

# export SOLID_SEMANTIC_SEARCH_API_TOKEN=token_48e46df9b9e3dc6251877724f8328c39da2158fc892846ab6710b1f29afe98eb
# export NLTK_DATA=venv/nltk_data
# export HF_HOME=models

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir setuptools wheel
pip install --no-cache-dir bs4 "fastapi[standard]" feedparser numpy
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
pip install --no-cache-dir nltk sentence_transformers sqlite_vec transformers

python -W ignore -m nltk.downloader -d venv/nltk_data punkt_tab averaged_perceptron_tagger_eng

mkdir -p db/ models/

if [ -n "$1" ] && [ "$1" == "--with-tests" ]; then
    pip install --no-cache-dir httpx pytest
fi
