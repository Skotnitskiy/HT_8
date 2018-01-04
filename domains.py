import random

import aiohttp
import asyncio
import numpy as np
from fake_useragent import UserAgent

proxies_list = ['http://50.203.239.27:80', 'http://50.203.239.28:80', 'http://192.116.142.153:8080',
                'http://50.203.239.24:80', 'http://50.203.239.23:80', 'http://50.203.239.29:80',
                'http://50.203.239.19:80', 'http://50.203.239.20:80', 'http://50.203.239.21:80',
                'http://50.203.239.22:80']


def get_pages_numbers():
    pages = 2000
    records_per_page = 25
    proxies = 10
    numbers = np.array(range(0, pages, records_per_page))
    np.random.shuffle(numbers)
    numbers = np.hsplit(numbers, proxies)
    last = np.append(numbers[0], pages)  # add last element to array
    numbers[0] = last
    return numbers


def get_text(link):
    return link.get('title')


def generate_user_agent():
    return UserAgent().random


async def get_pages(pg_numbers, prox):
    wait = 3 + random.random() * 2
    ua = generate_user_agent()
    url = "https://www.expireddomains.net/deleted-com-domains"
    results = []
    for number in pg_numbers:
        query = {"start": int(number)}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=query, proxy='http://192.116.142.153:8080', headers={'User-Agent': ua}) as resp:
                results.append(resp.text())
                print(resp.text())
                await asyncio.sleep(wait)
    return results


def get_tasks(pg_numbers, e_loop):
    tsks = []
    for pg_number, proxy in zip(pg_numbers, proxies_list):
        task = e_loop.create_task(get_pages(pg_numbers, proxy))
        tsks.append(task)
    return tsks


event_loop = asyncio.get_event_loop()
tasks = get_tasks(get_pages_numbers()[0], event_loop)
wait_tasks = asyncio.wait(tasks)
event_loop.run_until_complete(wait_tasks)
event_loop.close()
