import numpy as np


proxies_list = ['50.203.239.27:80', '50.203.239.28:80', '192.116.142.153:8080', '50.203.239.24:80', '50.203.239.23:80',
                '50.203.239.29:80', '50.203.239.19:80', '50.203.239.20:80', '50.203.239.21:80', '50.203.239.22:80']


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