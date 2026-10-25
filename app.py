
import json
import time

import requests
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="Quotes Scraper", page_icon="📚")

st.title("📚 Web Scraper for Quotes")
st.write("Extract quotes, authors, and tags from a public practice website.")

if st.button("Scrape Quotes"):
    all_quotes = []
    page = 1
    headers = {"User-Agent": "EducationalQuotesScraper/1.0"}

    try:
        progress = st.empty()

        while True:
            url = f"https://quotes.toscrape.com/page/{page}/"
            response = requests.get(
                url, headers=headers, timeout=15
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            quote_blocks = soup.select("div.quote")

            if not quote_blocks:
                break

            for item in quote_blocks:
                quote_text = item.select_one("span.text").get_text(strip=True)
                author = item.select_one("small.author").get_text(strip=True)
                tags = [
                    tag.get_text(strip=True)
                    for tag in item.select("a.tag")
                ]

                all_quotes.append({
                    "quote": quote_text,
                    "author": author,
                    "tags": tags
                })

            progress.write(f"Collected {len(all_quotes)} quotes...")
            page += 1
            time.sleep(1)

        progress.empty()

        if all_quotes:
            st.success(f"Successfully collected {len(all_quotes)} quotes!")

            st.subheader("Scraping Summary")
            st.write("**Total quotes:**", len(all_quotes))

            authors = [item["author"] for item in all_quotes]
            tags = [tag for item in all_quotes for tag in item["tags"]]

            if authors:
                st.write(
                    "**Most frequent author:**",
                    max(set(authors), key=authors.count)
                )

            if tags:
                st.write(
                    "**Most common tag:**",
                    max(set(tags), key=tags.count)
                )

            st.subheader("Collected Quotes")
            st.dataframe(all_quotes, use_container_width=True)

            json_data = json.dumps(
                all_quotes, indent=2, ensure_ascii=False
            )

            text_data = "\n\n".join(
                f'{item["quote"]}\n— {item["author"]}\n'
                f'Tags: {", ".join(item["tags"])}'
                for item in all_quotes
            )

            st.download_button(
                "Download JSON",
                data=json_data,
                file_name="quotes.json",
                mime="application/json"
            )

            st.download_button(
                "Download Text",
                data=text_data,
                file_name="quotes.txt",
                mime="text/plain"
            )
        else:
            st.warning("No quotes were found.")

    except requests.RequestException as error:
        st.error(f"Website request failed: {error}")
    except Exception as error:
        st.error(f"An error occurred: {error}")
