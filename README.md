# Web Scraper for Headlines & Quotes

A beginner-friendly Python project that collects quotes, authors, and tags from [Quotes to Scrape](https://quotes.toscrape.com/), a website made for practicing web scraping.

## Features
- HTTP GET requests with `requests`
- 10-second timeout and descriptive User-Agent header
- HTTP status checking with `raise_for_status()`
- HTML parsing with BeautifulSoup and CSS selectors
- Extracts quote text, author names, and tags
- Follows the Next pagination link
- Waits one second between page requests
- Handles timeout, HTTP, and network errors
- Saves data to `quotes.json` and `quotes.txt`
- Prints total count, most frequent author, and most common tag

## Requirements
- Python 3.10 or later
- Internet connection

## Files
- `scraper.py` — main scraper
- `requirements.txt` — required Python libraries
- `quotes.json` — generated JSON output
- `quotes.txt` — generated readable output

## Run on Windows (VS Code)
Open this folder in VS Code. In the terminal, run these commands one at a time:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scraper.py
```

If PowerShell blocks virtual-environment activation, skip the activation command and run the install and run commands.

## Source and responsible scraping
The source is `https://quotes.toscrape.com/`, a public practice website designed for scraping exercises. This program uses a timeout, identifies itself with a User-Agent, waits one second between requests, and does not access login-protected pages or collect personal data.

Before scraping any other website, review its terms of service and `robots.txt`, follow its rules, and keep requests slow. Do not scrape private or disallowed content.

## Troubleshooting
- **ModuleNotFoundError:** run `python -m pip install -r requirements.txt`.
- **Request error:** check your internet connection and try again later.
- **Python not recognized:** install Python and enable “Add Python to PATH”, or try `py` instead of `python`.

The website may change, so the number of collected quotes can vary.
