 # -*- coding: utf-8 -*-
import numpy as np
import requests
import random
from bs4 import BeautifulSoup as bs
import csv
import sys

delays = range(1,7,1)


HOST = 'https://www.b17.ru'
DELAY = np.random.choice(delays)
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',}

URL = "https://www.b17.ru/forum/?f=102"


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = "{}:{}".format(ip,port)
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def get_random_proxies():
    proxies = get_free_proxies() 
    for proxy in proxies:
        response = requests.get('https://ya.ru' )
        if response.status_code == requests.codes['ok']:
            return proxy
        else:
            continue

def write_to_csv(info_for_write):
    reload(sys)
    sys.setdefaultencoding('utf8')
    fields = ['topic id','topic name','number message', 'timestamp','txt msg', 'like', 'quote', 'who']  
    rows = [ [info_for_write['topic_id'], info_for_write['topic_name'], info_for_write['number_message'], info_for_write['likes'] , info_for_write['timestamp'] , info_for_write['txt_msg'] , info_for_write['quote'], info_for_write['who'] ]] 
    filename = "res.csv"
    with open('res.csv','a',newline='') as fout:
        writer=csv.writer(fout)    
        writer.writerows([tests.keys()])
        for row in zip(*tests.values()):
            row=[s.encode('utf-8') for s in row]
            writer.writerow([rows])
            