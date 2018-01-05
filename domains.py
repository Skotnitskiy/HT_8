import csv
import json
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


def write_to_csv(list_data):
    csv_file = 'domains.csv'
    csv_columns = ['domains']
    dict_data = [{'domains': data} for data in list_data]
    with open(csv_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(dict_data)


def write_json_to_txt(list_data):
    txt_file = 'domains.txt'
    data = [{'domain': data} for data in list_data]
    with open(txt_file, 'w') as f:
        json.dump(data, f)


pages = get_pages(get_pages_numbers())
domains = get_domains(pages)
write_to_csv(domains)
write_json_to_txt(domains)
