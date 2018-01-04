import numpy as np


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
