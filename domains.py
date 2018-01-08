import csv
import json
import random
import sqlite3

import numpy as np
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from openpyxl import Workbook


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
        try:
            pg = requests.get(url=url, params=param, headers={'User-Agent': ua}).text
        except ConnectionError:
            print(ConnectionError, "trying to connect via proxy")
            pg = requests.get(url=url, params=param, proxies={'https': '192.116.142.153:8080'},
                              headers={'User-Agent': ua}).text
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


def write_to_xlsx(rows):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Domains'
    xls_rows = ['domains'] + rows
    for r, value in zip(range(1, len(xls_rows)), xls_rows):
        ws.cell(row=r, column=1).value = value
    wb.save("domains.xlsx")


def write_to_db(rows):
    con = sqlite3.connect("domains.db")
    cursor = con.cursor()
    sql_delete_table = "DROP TABLE IF EXISTS domains"
    sql_create_table = "CREATE TABLE domains (domains text)"
    cursor.execute(sql_delete_table)
    con.commit()
    cursor.execute(sql_create_table)
    con.commit()
    for domain in rows:
        cursor.execute("INSERT INTO domains VALUES(:domains)", {'domains': domain})
        con.commit()
    con.close()


pages = get_pages(get_pages_numbers())
domains = get_domains(pages)
write_to_csv(domains)
write_json_to_txt(domains)
write_to_xlsx(domains)
write_to_db(domains)
