"""
Wizard Search - A TF-IDF and BERT-based search engine for Wikipedia pages.
"""

from flask import Flask, render_template, url_for, request, jsonify, redirect
import os
from pathlib import Path

import config
from search_engine import get_search_engine
from wikipedia_downloader import WikipediaDownloader


app = Flask(__name__)
app.config.from_object(config)

# Initialize search engine on startup (lazily loaded)
search_engine = None


def ensure_search_engine():
    """Ensure search engine is initialized."""
    global search_engine
    if search_engine is None:
        search_engine = get_search_engine(method=config.DEFAULT_EMBEDDING_METHOD)
    return search_engine


@app.route("/", methods=["GET", "POST"])
def index():
    """Main search page."""
    ensure_search_engine()

    if request.method == "POST":
        query = request.form.get("searchQuery", "").strip()
        method = request.form.get("method", config.DEFAULT_EMBEDDING_METHOD)

        if query:
            # Get search engine with selected method
            engine = get_search_engine(method=method)
            results = engine.search(query)

            return render_template(
                "index.html",
                results=results,
                query=query,
                method=method,
                play_sound=True
            )

    return render_template(
        "index.html",
        results=None,
        query="",
        method=config.DEFAULT_EMBEDDING_METHOD,
        play_sound=False
    )


@app.route('/files')
def list_files():
    """List all available files in the database."""
    ensure_search_engine()
    engine = get_search_engine()
    files = engine.get_available_files()

    return render_template(
        "files.html",
        files=files,
        total=len(files)
    )


@app.route('/page/<page_title>')
def view_page(page_title):
    """View a specific Wikipedia page."""
    filepath = os.path.join(config.FILES_DIR, page_title)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Format title: remove .txt extension and replace underscores
        display_title = page_title.replace('.txt', '').replace('_', ' ')

        return render_template(
            "page.html",
            title=display_title,
            body=content
        )

    except FileNotFoundError:
        return render_template(
            "error.html",
            error_message=f"Page '{page_title}' not found."
        ), 404

    except Exception as e:
        return render_template(
            "error.html",
            error_message=f"Error loading page: {str(e)}"
        ), 500


@app.route('/download', methods=['GET', 'POST'])
def download_pages():
    """Download new Wikipedia pages."""
    if request.method == 'POST':
        page_titles = request.form.get('pages', '').strip()

        if page_titles:
            # Split by newlines or commas
            titles = [t.strip() for t in page_titles.replace(',', '\n').split('\n')]
            titles = [t for t in titles if t]  # Remove empty strings

            if titles:
                downloader = WikipediaDownloader()
                downloader.download_pages(titles, delay=0.5)

                # Reload search engine to index new pages
                global search_engine
                search_engine = get_search_engine(force_reload=True)

                return render_template(
                    "download.html",
                    success=True,
                    count=len(titles)
                )

    return render_template("download.html", success=False)


@app.route('/api/search')
def api_search():
    """API endpoint for search (JSON response)."""
    ensure_search_engine()

    query = request.args.get('q', '').strip()
    method = request.args.get('method', config.DEFAULT_EMBEDDING_METHOD)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    engine = get_search_engine(method=method)
    results = engine.search(query)

    return jsonify({
        'query': query,
        'method': method,
        'results': [
            {'filename': filename, 'score': score}
            for filename, score in results
        ]
    })


@app.route('/stats')
def stats():
    """Show statistics about the search engine."""
    ensure_search_engine()
    engine = get_search_engine()
    files = engine.get_available_files()

    return render_template(
        "stats.html",
        total_pages=len(files),
        method=engine.method,
        files=files
    )


# Cache busting for static files
@app.context_processor
def override_url_for():
    """Remove CSS cache for development."""
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """Add timestamp to static file URLs to prevent caching."""
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            if os.path.exists(file_path):
                values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("error.html", error_message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template("error.html", error_message="Internal server error"), 500


if __name__ == "__main__":
    app.run(debug=config.DEBUG)