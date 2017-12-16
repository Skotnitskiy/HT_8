from bs4 import BeautifulSoup
import requests

quotes_to_scrape_url = "http://quotes.toscrape.com"
quotes_page = requests.get(quotes_to_scrape_url)
soup = BeautifulSoup(quotes_page.text, "html.parser")

quotes = soup.select("div.quote")
for quote in quotes:
    quote_text = quote.select("span.text")[0].text[1:-1]
    author_url = quote.select("span > a")[0].get("href")
    author_title = quote.select("span > small")[0].text
    author_page = requests.get(quotes_to_scrape_url + author_url)
    author_soup = BeautifulSoup(author_page.text, "html.parser")
    author_born_date = author_soup.select("span.author-born-date")[0].text
    author_born_place = author_soup.select("span.author-born-location")[0].text[2:]
    author_about = author_soup.select("div.author-description")[0].text.strip()
    tags = quote.select("a.tag")
    for tag in tags:
        tag_name = tag.text
        tag_url = tag.get("href")
