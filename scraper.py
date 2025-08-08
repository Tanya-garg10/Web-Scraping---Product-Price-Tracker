# scraper.py
import requests
from bs4 import BeautifulSoup
import re

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
    if price_tag:
        price_text = price_tag.text
        # Extract numeric part
        price = int(re.sub(r"[^\d]", "", price_text))
        return price
    else:
        return None
