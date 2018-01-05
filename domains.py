import random
import numpy as np
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_pages_numbers():
    pages = 75
    records_per_page = 25
    numbers = np.array(range(0, pages, records_per_page))
    np.random.shuffle(numbers)
    numbers = list(numbers)
    numbers.append(pages)
    return numbers


def get_text(link):
    return link.get('title')


def generate_user_agent():
    return UserAgent().random


def get_pages(pg_numbers):
    ua = generate_user_agent()
    url = "https://www.expireddomains.net/deleted-com-domains"
    results = []
    for number in pg_numbers:
        wait = 3 + random.random() * 2
        param = {'start': number}
        pg = requests.get(url=url, params=param, headers={'User-Agent': ua}).text
        results.append(pg)
        time.sleep(wait)
        print('page with number', number, 'received')
    return results


def get_domains(pgs):
    results = []
    for page in pgs:
        soup = BeautifulSoup(page, "html.parser")
        links = soup.select("a.namelinks")
        if links:
            domains = list(map(get_text, links))
            print('parsed', len(domains), 'records')
            for domain in domains:
                results.append(domain)
        else:
            print('Page is empty', page)
    return results


pages = get_pages(get_pages_numbers())
print(get_domains(pages))
