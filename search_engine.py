"""
Improved search engine with TF-IDF and BERT embeddings support.
"""

import string
import math
import os
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

import config


class SearchEngine:
    """Search engine supporting both TF-IDF and BERT embeddings."""

    def __init__(self, method='tfidf'):
        """
        Initialize the search engine.

        Args:
            method: 'tfidf' or 'bert' for the embedding method
        """
        self.method = method
        self.files_dir = config.FILES_DIR
        self.stopwords = self._load_stopwords()
        self.documents = []
        self.filenames = []
        self.doc_vectors = []

        # Load BERT model if needed
        if self.method == 'bert':
            self._load_bert_model()

        self._index_documents()

    def _load_stopwords(self) -> set:
        """Load stopwords from file."""
        try:
            with open(config.STOPWORDS_FILE, 'r') as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            print("Warning: Stopwords file not found. Using empty set.")
            return set()

    def _load_bert_model(self):
        """Load BERT model for embeddings."""
        try:
            from sentence_transformers import SentenceTransformer
            print("Loading BERT model...")
            self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("BERT model loaded successfully!")
        except ImportError:
            print("Warning: sentence-transformers not installed. Install with: pip install sentence-transformers")
            print("Falling back to TF-IDF method.")
            self.method = 'tfidf'
        except Exception as e:
            print(f"Error loading BERT model: {e}")
            print("Falling back to TF-IDF method.")
            self.method = 'tfidf'

    def _clean_word(self, word: str) -> str:
        """Clean a word by removing punctuation and converting to lowercase."""
        cleaned = ''.join(ch for ch in word
                         if ch not in (string.punctuation + "1234567890-+_\n\t"))
        return cleaned.lower()

    def _tokenize_and_count(self, filepath: str) -> Dict[str, int]:
        """Tokenize a document and count word frequencies."""
        word_count = {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into words
            words = content.split()

            for word in words:
                cleaned_word = self._clean_word(word)

                # Skip stopwords and short words
                if cleaned_word and len(cleaned_word) >= 2 and cleaned_word not in self.stopwords:
                    word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1

        except Exception as e:
            print(f"Error reading file {filepath}: {e}")

        return word_count

    def _index_documents(self):
        """Index all documents in the files directory."""
        files_path = Path(self.files_dir)

        # Get all .txt files (excluding subdirectories like qualityFiles)
        txt_files = [f for f in files_path.glob('*.txt') if f.is_file()]

        if not txt_files:
            print("Warning: No documents found to index!")
            return

        for filepath in sorted(txt_files):
            self.filenames.append(filepath.name)

            if self.method == 'tfidf':
                # Create word count dictionary for TF-IDF
                doc_dict = self._tokenize_and_count(str(filepath))
                self.documents.append(doc_dict)

            elif self.method == 'bert':
                # Read full text for BERT embedding
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                    self.documents.append(text)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    self.documents.append("")

        # Generate BERT embeddings if using BERT method
        if self.method == 'bert' and hasattr(self, 'bert_model'):
            print("Generating BERT embeddings for documents...")
            self.doc_vectors = self.bert_model.encode(self.documents, show_progress_bar=True)
            print(f"Indexed {len(self.doc_vectors)} documents with BERT embeddings.")
        else:
            print(f"Indexed {len(self.documents)} documents with TF-IDF.")

    def _calculate_idf(self, word: str) -> float:
        """Calculate IDF (Inverse Document Frequency) for a word."""
        doc_count = sum(1 for doc in self.documents if word in doc)
        return math.log10(len(self.documents) / (doc_count + 1) + 1)

    def _calculate_tfidf_scores(self, query: str) -> List[float]:
        """Calculate TF-IDF scores for a query against all documents."""
        query_words = [self._clean_word(word) for word in query.split()]
        query_words = [w for w in query_words if w and w not in self.stopwords]

        if not query_words:
            return [0.0] * len(self.documents)

        scores = []

        for doc in self.documents:
            score = 0.0
            for word in query_words:
                if word in doc:
                    # TF: log(1 + term frequency)
                    tf = math.log10(1 + doc[word])
                    # IDF: inverse document frequency
                    idf = self._calculate_idf(word)
                    score += tf * idf
            scores.append(score)

        return scores

    def _calculate_bert_scores(self, query: str) -> List[float]:
        """Calculate cosine similarity scores using BERT embeddings."""
        if not hasattr(self, 'bert_model'):
            return [0.0] * len(self.documents)

        # Encode query
        query_vector = self.bert_model.encode([query])[0]

        # Calculate cosine similarity with all documents
        scores = []
        for doc_vector in self.doc_vectors:
            # Cosine similarity
            similarity = np.dot(query_vector, doc_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(doc_vector)
            )
            scores.append(float(similarity))

        return scores

    def search(self, query: str, top_k: int = None) -> List[Tuple[str, float]]:
        """
        Search for documents matching the query.

        Args:
            query: Search query string
            top_k: Number of top results to return (default from config)

        Returns:
            List of (filename, score) tuples sorted by relevance
        """
        if not query or not query.strip():
            return []

        if top_k is None:
            top_k = config.TOP_K_RESULTS

        # Calculate scores based on method
        if self.method == 'bert':
            scores = self._calculate_bert_scores(query)
        else:
            scores = self._calculate_tfidf_scores(query)

        # Combine filenames with scores
        results = list(zip(self.filenames, scores))

        # Sort by score (descending) and return top k
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def get_available_files(self) -> List[str]:
        """Get list of all indexed files."""
        return self.filenames.copy()


# Global search engine instance
_search_engine = None


def get_search_engine(method=None, force_reload=False) -> SearchEngine:
    """
    Get or create the global search engine instance.

    Args:
        method: 'tfidf' or 'bert' (default from config)
        force_reload: Force reload the search engine

    Returns:
        SearchEngine instance
    """
    global _search_engine

    if method is None:
        method = config.DEFAULT_EMBEDDING_METHOD

    if _search_engine is None or force_reload:
        _search_engine = SearchEngine(method=method)

    return _search_engine


def search(query: str, method=None) -> List[Tuple[str, float]]:
    """
    Convenience function for searching.

    Args:
        query: Search query
        method: 'tfidf' or 'bert' (optional)

    Returns:
        List of (filename, score) tuples
    """
    engine = get_search_engine(method=method)
    return engine.search(query)
