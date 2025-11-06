# Wizard Search - Enhanced TF-IDF & BERT Search Engine

An intelligent search engine for Wikipedia pages supporting both **TF-IDF** and **BERT embeddings**, built with Flask 3.0 and Python.

![Wizard Search](static/img/wizardsearch.png)

## 🎯 Features

### ✨ What's New

- **🤖 BERT Embeddings**: Choose between traditional TF-IDF or modern BERT semantic search
- **📥 Download More Pages**: Built-in Wikipedia downloader to expand your database
- **⚡ Flask 3.0**: Updated to latest Flask framework
- **🎨 Modern UI**: Improved interface with method selection and score display
- **📊 Statistics**: View search engine stats and browse all indexed pages
- **🔍 REST API**: JSON API endpoint for programmatic access

## 🚀 Quick Start

### Installation

```sh
# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 app.py
```

Visit `http://localhost:5000` in your browser!

### Download More Wikipedia Pages

```sh
# Download specific pages
python3 wikipedia_downloader.py --pages "Artificial_intelligence" "Python_(programming_language)"

# List all downloaded pages
python3 wikipedia_downloader.py --list
```

## 📖 Usage

### Web Interface

1. **Search**: Enter your query and select TF-IDF or BERT method
2. **Browse**: View all indexed Wikipedia pages
3. **Download**: Add custom Wikipedia pages to expand your database
4. **Stats**: Check search engine statistics

### Search Methods

- **TF-IDF**: Fast, lightweight keyword-based search
  - Best for: Exact term matching, fast queries

- **BERT**: Semantic understanding using AI embeddings
  - Best for: Meaning-based search, related concepts
  - Requires: `pip install sentence-transformers torch`

### Python API

```python
from search_engine import search

# Search with TF-IDF
results = search("clouds weather", method="tfidf")

# Results: [(filename, score), ...]
for filename, score in results[:5]:
    print(f"{filename}: {score:.3f}")
```

### REST API

```sh
curl "http://localhost:5000/api/search?q=rainbow&method=tfidf"
```

## 📚 Current Database

The database currently includes 7 Wikipedia pages:
- Bread
- Clouds
- Hot Dog
- Norway
- Rainbow
- Sun
- Television

**Expand it!** Use the download feature to add more pages on any topic.

## 🛠️ Tech Stack

- **Flask 3.0**: Modern Python web framework
- **Python 3.8+**: Core language
- **Sentence Transformers**: BERT embeddings (optional)
- **NumPy**: Numerical computations
- **Requests**: Wikipedia API integration
- **HTML/CSS/JavaScript**: Retro-styled frontend

## 📁 Project Structure

```
Wizard_Search/
├── app.py                    # Flask application
├── search_engine.py          # Search engine (TF-IDF & BERT)
├── wikipedia_downloader.py   # Wikipedia page downloader
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── files/                    # Wikipedia pages database
├── templates/                # HTML templates
└── static/                   # CSS, images, JS
```

## 🎓 How It Works

### TF-IDF Method
1. **Tokenization**: Split documents, remove stopwords
2. **Term Frequency**: Count term occurrences
3. **IDF**: Weight by term rarity across documents
4. **Scoring**: Rank by TF × IDF

### BERT Method
1. **Embeddings**: Convert to vector representations
2. **Semantic**: Capture meaning beyond keywords
3. **Similarity**: Cosine similarity scoring
4. **Ranking**: Return most semantically similar

## 🤝 Contributing

Contributions welcome! Feel free to add features, improve algorithms, or expand the database.

## 📝 License

MIT License

## 👤 Author

**Thomas Ramirez**

Enhanced with modern features:
- BERT semantic search
- Wikipedia downloader
- Flask 3.0 upgrade
- Improved architecture

---

**Click the logo for a surprise!** 🧙‍♂️✨

