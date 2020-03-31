 # -*- coding: utf-8 -*-
import numpy as np
import requests
import random
from bs4 import BeautifulSoup as bs
import csv
import os 


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

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()



def write_to_csv(info_for_write):
    #notice use OrderedDict for save order
	fields = ['topic id','topic name','number message','timestamp','txt msg','like','quote','who']
	file = 'out.csv'
	with open(file,'a+',encoding='utf-8-sig',newline='') as f:
		csv_dict = [row for row in csv.DictReader(f)]
		w = csv.DictWriter(f,fieldnames=fields)
		if os.stat(file).st_size == 0:
    			w.writeheader()
		w.writerow(info_for_write)
