# ============================================================
# CRAWLER
# ============================================================

import requests
from robots import allowed_by_robots
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from Indexer import index_page
import time

HEADERS = {
    "User-Agent": "MiniSearchBot/1.0"
}


def crawl(start_urls, max_pages=100):

    queue = list(start_urls)

    visited = set()

    session = requests.Session()

    while queue and len(visited) < max_pages:

        url = queue.pop(0)

        if url in visited:
            continue

        visited.add(url)

        print("Crawling:", url)

        try:

            if not allowed_by_robots(url):
                print("Blocked by robots.txt:", url)
                continue

            response = session.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                continue

            content_type = response.headers.get(
                "content-type",
                ""
            )

            if "text/html" not in content_type:
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Remove things that aren't useful page text
            for tag in soup([
                "script",
                "style",
                "noscript",
                "header",
                "footer"
            ]):
                tag.decompose()

            title = soup.title.string.strip() if soup.title and soup.title.string else url

            text = soup.get_text(
                " ",
                strip=True
            )

            # Save page to index
            index_page(
                url,
                title,
                text
            )

            print("Indexed:", title)

            # Find links
            for link in soup.find_all("a", href=True):

                next_url = urljoin(
                    url,
                    link["href"]
                )

                parsed = urlparse(next_url)

                # Only HTTP/HTTPS
                if parsed.scheme not in ("http", "https"):
                    continue

                # Remove fragments
                next_url = next_url.split("#")[0]

                if next_url not in visited:
                    queue.append(next_url)

            # Be polite to websites
            time.sleep(1)

        except Exception as e:

            print("Error:", e)
