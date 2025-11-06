"""
Script to download Wikipedia pages for the search engine.
"""

import os
import time
import argparse
from pathlib import Path
import requests

import config


class WikipediaDownloader:
    """Downloads and manages Wikipedia pages."""

    def __init__(self, output_dir=None):
        """
        Initialize the downloader.

        Args:
            output_dir: Directory to save downloaded pages (default: config.FILES_DIR)
        """
        self.output_dir = output_dir or config.FILES_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_filename(self, page_title: str) -> str:
        """Convert Wikipedia page title to valid filename."""
        # Replace spaces with underscores and remove invalid characters
        filename = page_title.replace(' ', '_')
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename + '.txt'

    def download_page(self, page_title: str, retries=3) -> bool:
        """
        Download a single Wikipedia page using Wikipedia API.

        Args:
            page_title: Title of the Wikipedia page
            retries: Number of retries on failure

        Returns:
            True if successful, False otherwise
        """
        # Clean title for filename
        filename = self.clean_filename(page_title)
        filepath = os.path.join(self.output_dir, filename)

        # Skip if already exists
        if os.path.exists(filepath):
            print(f"  ⏭️  Skipping {page_title} (already exists)")
            return True

        # Wikipedia API endpoint
        api_url = "https://en.wikipedia.org/w/api.php"

        for attempt in range(retries):
            try:
                print(f"  📥 Downloading: {page_title}...", end=' ', flush=True)

                # Parameters for Wikipedia API
                params = {
                    'action': 'query',
                    'format': 'json',
                    'titles': page_title.replace('_', ' '),
                    'prop': 'extracts',
                    'explaintext': True,
                    'redirects': 1
                }

                # Headers with User-Agent (required by Wikipedia)
                headers = {
                    'User-Agent': 'WizardSearch/1.0 (Educational Project; Python/Requests)'
                }

                # Make request
                response = requests.get(api_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()

                data = response.json()

                # Extract page content
                pages = data.get('query', {}).get('pages', {})

                if not pages:
                    print(f"❌ Failed: No data returned")
                    return False

                # Get first page (should be only one)
                page_data = next(iter(pages.values()))

                # Check if page exists
                if 'missing' in page_data:
                    print(f"❌ Failed: Page not found")
                    return False

                # Get content
                content = page_data.get('extract', '')

                if not content:
                    print(f"❌ Failed: Empty content")
                    return False

                # Save to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"✅ Success! ({len(content)} chars)")
                return True

            except requests.exceptions.Timeout:
                print(f"⚠️  Timeout, retrying..." if attempt < retries - 1 else f"❌ Failed: Timeout")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return False

            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    print(f"⚠️  Error, retrying... ({e})")
                    time.sleep(2)
                else:
                    print(f"❌ Failed after {retries} attempts: {e}")
                return False

            except Exception as e:
                if attempt < retries - 1:
                    print(f"⚠️  Error, retrying... ({e})")
                    time.sleep(2)
                else:
                    print(f"❌ Failed after {retries} attempts: {e}")
                return False

        return False

    def download_pages(self, page_titles: list, delay=1.0):
        """
        Download multiple Wikipedia pages.

        Args:
            page_titles: List of page titles to download
            delay: Delay between downloads (seconds) to be polite to Wikipedia
        """
        print(f"\n{'='*60}")
        print(f"📚 Wikipedia Page Downloader")
        print(f"{'='*60}")
        print(f"Output directory: {self.output_dir}")
        print(f"Pages to download: {len(page_titles)}\n")

        successful = 0
        failed = 0

        for i, title in enumerate(page_titles, 1):
            print(f"[{i}/{len(page_titles)}]", end=' ')

            if self.download_page(title):
                successful += 1
            else:
                failed += 1

            # Be polite to Wikipedia servers
            if i < len(page_titles):
                time.sleep(delay)

        print(f"\n{'='*60}")
        print(f"✅ Successfully downloaded: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Total files in database: {len(self.get_downloaded_pages())}")
        print(f"{'='*60}\n")

    def get_downloaded_pages(self) -> list:
        """Get list of all downloaded Wikipedia pages."""
        files_path = Path(self.output_dir)
        txt_files = [f.stem for f in files_path.glob('*.txt') if f.is_file()]
        return sorted(txt_files)

    def download_default_pages(self):
        """Download the default set of Wikipedia pages from config."""
        print("Downloading default Wikipedia pages...")
        self.download_pages(config.DEFAULT_WIKIPEDIA_PAGES)

    def download_custom_pages(self, page_titles: list):
        """Download custom list of Wikipedia pages."""
        print(f"Downloading {len(page_titles)} custom pages...")
        self.download_pages(page_titles)

    def list_downloaded_pages(self):
        """Print list of all downloaded pages."""
        pages = self.get_downloaded_pages()
        print(f"\n📚 Downloaded Wikipedia Pages ({len(pages)} total):")
        print("=" * 60)
        for i, page in enumerate(pages, 1):
            print(f"{i:3d}. {page.replace('_', ' ')}")
        print("=" * 60 + "\n")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Download Wikipedia pages for Wizard Search'
    )

    parser.add_argument(
        '--default',
        action='store_true',
        help='Download default set of Wikipedia pages (150 pages)'
    )

    parser.add_argument(
        '--pages',
        nargs='+',
        help='Specific Wikipedia page titles to download'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all downloaded pages'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between downloads in seconds (default: 1.0)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for downloaded pages'
    )

    args = parser.parse_args()

    downloader = WikipediaDownloader(output_dir=args.output)

    if args.list:
        downloader.list_downloaded_pages()
    elif args.default:
        downloader.download_default_pages()
    elif args.pages:
        downloader.download_custom_pages(args.pages)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # Download default 150 pages:")
        print("  python wikipedia_downloader.py --default")
        print("\n  # Download specific pages:")
        print("  python wikipedia_downloader.py --pages 'Python_(programming_language)' 'Artificial_intelligence'")
        print("\n  # List downloaded pages:")
        print("  python wikipedia_downloader.py --list")


if __name__ == '__main__':
    main()
