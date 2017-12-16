import csv
import requests
from bs4 import BeautifulSoup


def write_headers_to_csv(csv_file, csv_columns):
    with open(csv_file, 'a') as dump:
        writer = csv.DictWriter(dump, fieldnames=csv_columns)
        writer.writeheader()


def write_dict_to_csv(csv_file, csv_columns, dict_data):
    with open(csv_file, 'a') as dump:
        writer = csv.DictWriter(dump, fieldnames=csv_columns)
        writer.writerow(dict_data)


quotes_to_scrape_url = "http://quotes.toscrape.com"
page_number = 1
has_next = True
columns = ["Quote", "Author", "AuthorUrl", "AuthorBornDate", "AuthorBornPlace", "Tags", "AboutAuthor"]
write_headers_to_csv("dump.csv", columns)
tag_separator = "@"
while has_next:
    quotes_page = requests.get(quotes_to_scrape_url + "/page/{}".format(page_number))
    soup = BeautifulSoup(quotes_page.text, "html.parser")
    quotes = soup.select("div.quote")
    if len(quotes) > 0:
        for quote in quotes:
            quote_text = quote.select("span.text")[0].text[1:-1]
            author_url = quote.select("span > a")[0].get("href")
            author_title = quote.select("span > small")[0].text
            author_page = requests.get(quotes_to_scrape_url + author_url)
            author_soup = BeautifulSoup(author_page.text, "html.parser")
            author_born_date = author_soup.select("span.author-born-date")[0].text
            author_born_place = author_soup.select("span.author-born-location")[0].text[2:]
            author_about = author_soup.select("div.author-description")[0].text.strip()
            quote_tags = quote.select("a.tag")
            result_tag_str = ""
            for tag in quote_tags:
                tag_name = tag.text
                tag_url = tag.get("href")
                result_tag_str += tag_separator.join((tag_name, tag_url)) + "\n"
            csv_data = {"Quote": quote_text, "Author": author_title, "AuthorUrl": author_url,
                        "AuthorBornDate": author_born_date, "AuthorBornPlace": author_born_place,
                        "Tags": result_tag_str,
                        "AboutAuthor": author_about}
            write_dict_to_csv("dump.csv", columns, csv_data)
    else:
        has_next = False
    page_number += 1

