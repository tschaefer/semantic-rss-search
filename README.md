# A Solid Semantic Search for RSS Feeds 🗞️

Index and search RSS feeds using semantic search techniques.
This API provides endpoints to embed RSS feed entries into a vector database
and search them based on semantic similarity.

### Index RSS Feeds

Index RSS feeds by posting their URLs to the `/embed` endpoint. This will
parse the feed entries and store title, summary, published date, link, and
vector embeddings in the database. The vector embeddings are based on the
content of the title and summary.

The endpoint requires authorization with a bearer token, which must be set
as an environment variable `SEMANTIC_RSS_SEARCH_API_TOKEN`.

### Search RSS Feeds

Search indexed RSS feeds by posting a query to the `/search` endpoint.
The search will return the top `k` entries that match the query based on
semantic similarity. The results include the title, summary, published date,
link, distance from the query vector, and the number of tokens of the indexed
content.

### Technology Stack

- [**FastAPI**](https://fastapi.tiangolo.com): For building the API endpoints.
- [**SQLite Vector**](https://alexgarcia.xyz/sqlite-vec/): For storing vector embeddings in a SQLite database.
- [**Sentence Transformers**](https://www.sbert.net): For generating vector embeddings from text.
- [**bge-base-en-v1.5**](https://huggingface.co/BAAI/bge-base-en-v1.5): A pre-trained model optimised for semantic search and passage retrieval (768-dimensional embeddings).

## Getting Started

### Prerequisites

An environment to run containerized applications, such as Docker or
Kubernetes.

For local development, you need [Python 3.11](https://www.python.org) or later.
Set up the necessary environment by running the script `setup.sh`. This will
create a [virtual environment](https://docs.python.org/3/library/venv.html)
and install the required dependencies.

```bash
bash setup.sh
```

For running tests execute the setup script using the `--with-tests` flag.
This will install additional dependencies.

```bash
bash setup.sh --with-tests
```

### Running with Docker

```bash
docker run --detach \
  --name semantic-rss-search \
  --publish 8000:8000 \
  --environment SEMANTIC_RSS_SEARCH_API_TOKEN=your_token_here \
  --volume ./models:/app/models \
  --volume ./db:/app/db \
  ghcr.io/tschaefer/semantic-rss-search:latest
```

### Running Locally

Export the required environment variables.

```bash
export SEMANTIC_RSS_SEARCH_API_TOKEN=your_token_here
export NLTK_DATA=venv/nltk_data
export HF_HOME=models
```

Activate the virtual environment.

```bash
source venv/bin/activate
```

Run the production server using FastAPI and Uvicorn.

```bash
python run.py
```

For development purposes, you can run FastAPI with hot reloading and
additional logging information.

```bash
fastapi run app/main.py
```

> [!NOTE]
> On first run, the application will download the pre-trained model.


### Running Tests

To run the tests, ensure you have installed the additional dependencies, see
the **Prerequisites** section. Then execute the tests using `pytest` with a
temporary SQLite database.

```bash
SEMANTIC_RSS_SEARCH_DB=/tmp/semantic_rss_search.db pytest -v tests/
rm -f /tmp/semantic_rss_search.db
```

## Usage

Find the API documentation at http://localhost:8000/redoc.

### Indexing RSS Feeds

```bash
curl --silent --include \
    --header "Authorization: Bearer token_48e46df9b9e3dc6251877724f8328c39da2158fc892846ab6710b1f29afe98eb" \
    --json '{ "url": "https://www.theregister.com/headlines.atom" }' \
    http://localhost:8000/embed

HTTP/1.1 201 Created
date: Wed, 28 May 2025 19:14:49 GMT
server: uvicorn
content-length: 14
content-type: application/json

{"entries":50}
```

### Searching RSS Feeds

```bash
curl --silent \
    --json '{ "query": "Is using AI an energy waste?", "k": 3 }' \
    http://localhost:8000/search
{
  "query": "Is using AI an energy waste?",
  "k": 3,
  "results": [
    {
      "title": "AI's enormous energy appetite can be curbed, but only through lateral thinking",
      "summary": "...",
      "published": 1748331006,
      "link": "https://go.theregister.com/feed/www.theregister.com/2025/05/27/opinion_column_ai_energy/",
      "distance": 0.7886583209037781,
      "token": 117
    },
    {
      "title": "'Some Signs of AI Model Collapse Begin To Reveal Themselves'",
      "summary": "...",
      "published": 1748433783,
      "link": "https://slashdot.org/story/25/05/28/0242240/some-signs-of-ai-model-collapse-begin-to-reveal-themselves?utm_source=rss1.0mainlinkanon&utm_medium=feed",
      "distance": 0.8932643532752991,
      "token": 525
    },
    {
      "title": "Nothing's Carl Pei Says Your Smartphone's OS Will Replace All of Its Apps",
      "summary": "...",
      "published": 1748433783,
      "link": "https://mobile.slashdot.org/story/25/05/28/0316239/nothings-carl-pei-says-your-smartphones-os-will-replace-all-of-its-apps?utm_source=rss1.0mainlinkanon&utm_medium=feed",
      "distance": 0.906494677066803,
      "token": 421
    }
  ]
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
For major changes, open an issue first to discuss what you would like to change.

Ensure that your code adheres to the existing style and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).
