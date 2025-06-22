# Code to scrape the data from the Russell Tennis Center website
import os
import requests
from bs4 import BeautifulSoup

# Dictionary of URLs to scrape (includes all pages of the website)
pages = {
    "home": "https://russelltenniscenter.com/",
    "programs": "https://russelltenniscenter.com/programs",
    "junior program": "https://russelltenniscenter.com/junior-program",
    "adult program": "https://russelltenniscenter.com/adult-program",
    "summer camp": "https://russelltenniscenter.com/summer-camp",
    "about": "https://russelltenniscenter.com/about-us",
    "contact": "https://russelltenniscenter.com/contact-us",
}

# Function to clean the text
def clean_text(html):
    """Extract visible text and clean it up."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove unecessary website features (tags: nav, footers, scripts, styles)
    for tag in soup(["nav", "footer", "script", "style"]):
        tag.decompose()
    # Grab only visible text
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

# Scrape and save the data
for name, url in pages.items():
    file_path = f"data/{name}.txt"
    if os.path.exists(file_path):
        print(f" Skipped (already exists): {file_path}\n")
        continue
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        text = clean_text(response.text)

        with open(f"data/{name}.txt", "w", encoding="utf-8") as file:
            file.write(text)
            print(f" Saved: data/{name}.txt\n")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

