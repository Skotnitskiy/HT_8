from bs4 import BeautifulSoup
import requests

quotes_toscrape_url = "http://quotes.toscrape.com"
quotes_page = requests.get(quotes_toscrape_url)
soup = BeautifulSoup(quotes_page.text, "html.parser")
quote = soup.select("div.quote")[0]  # loop
quote_text = quote.select("span.text")[0].text[1:-1]
author_url = quote.select("span > a")[0].get("href")
author_title = quote.select("span > small")[0].text
author_page = requests.get(quotes_toscrape_url + author_url)
author_soup = BeautifulSoup(author_page.text, "html.parser")
author_born_date = author_soup.select("span.author-born-date")[0].text
author_born_place = author_soup.select("span.author-born-location")[0].text[2:]
author_about = author_soup.select("div.author-description")[0].text
# tags = quote.select("a.tag")
# for tag in tags:
#     tag_name = tag.text
#     tag_url = tag.get("href")
#     print(tag_name, tag_url)

