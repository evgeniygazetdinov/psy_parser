#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

URL = "https://www.b17.ru/forum/?f=102"
HOST = 'https://www.b17.ru'

def one_paginate():
	pass


def get_info_from_topic(topic):
	page = requests.get(HOST+topic)
	soup = BeautifulSoup(page.content)
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info
	
def parse_one_table(table):
	pass

def extract_from_topic(topic):
	print("EXTRACT")
	info = get_info_from_topic(topic)
	parse_one_table(info[0])


def forum_checker(URL):
	#get all from one paginate pagegit
	forum_links = []
	page = requests.get(URL)
	data = page.content
	soup = BeautifulSoup(data,"lxml")
	for link in soup.find_all('a'):
		forum_links.append(link.get('href'))
	l = list(filter(None, forum_links))
	res = [x for x in l if re.search("id", x)]
	print(res)
	print(len(res))
	return res

def main():
	topics = forum_checker(URL)
	for topic in topics[0:2]:
		print('HERE')
		extract_from_topic(topic)
	print("this main")




if __name__ == "__main__":
	main()
