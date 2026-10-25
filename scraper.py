"""
Web Scraper for Headlines & Quotes
Practice source: https://quotes.toscrape.com
"""
import json
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "StudentLearningProject/1.0 (polite educational scraper)"}
TIMEOUT_SECONDS = 10
REQUEST_DELAY_SECONDS = 1


def fetch_page(url):
    """Fetch and parse one page, reporting common request errors."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.Timeout:
        print(f"Timeout while requesting: {url}")
    except requests.exceptions.HTTPError as exc:
        print(f"HTTP error while requesting {url}: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"Request failed for {url}: {exc}")
    return None


def scrape_quotes(max_pages=None):
    """Collect quotes, authors and tags, following pagination."""
    url = BASE_URL
    quotes = []
    pages = 0

    while url and (max_pages is None or pages < max_pages):
        print(f"Fetching page {pages + 1}: {url}")
        soup = fetch_page(url)
        if soup is None:
            break

        for item in soup.select("div.quote"):
            quote_text = item.select_one("span.text")
            author = item.select_one("small.author")
            if quote_text is None or author is None:
                continue
            quotes.append({
                "text": quote_text.get_text(strip=True),
                "author": author.get_text(strip=True),
                "tags": [tag.get_text(strip=True) for tag in item.select("a.tag")],
            })

        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link.get("href")) if next_link else None
        pages += 1
        if url and (max_pages is None or pages < max_pages):
            time.sleep(REQUEST_DELAY_SECONDS)

    return quotes


def save_results(quotes):
    """Write JSON and readable text output."""
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)

    with open("quotes.txt", "w", encoding="utf-8") as file:
        if not quotes:
            file.write("No quotes collected. Check your internet connection and try again.\n")
        for index, quote in enumerate(quotes, start=1):
            file.write(f"{index}. {quote['text']}\n")
            file.write(f"   Author: {quote['author']}\n")
            file.write(f"   Tags: {', '.join(quote['tags']) if quote['tags'] else 'None'}\n\n")


def print_summary(quotes):
    print("\n--- Scraping Summary ---")
    print(f"Total quotes collected: {len(quotes)}")
    authors = Counter(q["author"] for q in quotes)
    tags = Counter(tag for q in quotes for tag in q["tags"])
    if authors:
        name, count = authors.most_common(1)[0]
        print(f"Most frequent author in collected records: {name} ({count})")
    else:
        print("Most frequent author: Not available")
    if tags:
        name, count = tags.most_common(1)[0]
        print(f"Most common tag: {name} ({count})")
    else:
        print("Most common tag: Not available")


def main():
    print("Web Scraper for Headlines & Quotes")
    print("Practice source: https://quotes.toscrape.com/\n")
    quotes = scrape_quotes()  # Use max_pages=2 here to test only two pages.
    save_results(quotes)
    print("\nSaved quotes.json and quotes.txt")
    print_summary(quotes)


if __name__ == "__main__":
    main()
