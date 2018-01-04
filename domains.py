import random

import aiohttp
import asyncio
import numpy as np
import requests
import time
from fake_useragent import UserAgent

proxies_list = ['http://50.203.239.27:80', 'http://50.203.239.28:80', 'http://192.116.142.153:8080',
                'http://50.203.239.24:80', 'http://50.203.239.23:80', 'http://50.203.239.29:80',
                'http://50.203.239.19:80', 'http://50.203.239.20:80', 'http://50.203.239.21:80',
                'http://50.203.239.22:80']


def get_pages_numbers():
    pages = 2000
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
        requests.get(url=url, params=param, headers={'User-Agent': ua})
        time.sleep(wait)
        print('page with', number, 'received')
    return results


get_pages(get_pages_numbers())
