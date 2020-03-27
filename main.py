#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict



URL = "https://www.b17.ru/forum/?f=102"
HOST = 'https://www.b17.ru'

def one_paginate():
	pass


def get_info_from_topic(topic):
	page = requests.get(HOST+topic)
	soup = BeautifulSoup(page.content,features="lxml")
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info

def get_topic_id(from_topic):
	raw_topic = re.findall(r'\w{2}=\S\w{4}_\d+',str(from_topic))
	if raw_topic:
		topic_id = raw_topic[0].split('id="post_')
		return topic_id[1]
	return 


def parse_one_table(table):
	#extract values
	#rebuild regexp
	topic_id = get_topic_id(table)
	print(topic_id)
	

def extract_from_topic(topic):
	info = get_info_from_topic(topic)
	for info_for_write in info:
			parse_one_table(info_for_write)

def forum_checker(URL):
	#get all from one paginate pagegit
	forum_links = OrderedDict()
	page = requests.get(URL)
	data = page.content
	soup = BeautifulSoup(data,"lxml")
	for link in soup.find_all('a'):
		#include topic links 
		if re.search("id", str(link.get('href'))):
			#filter segonia \minutu na
			# zad \
			if re.match(r'Сегодня',str((link.contents)[0])):
				continue
			if re.match(r'\d{1}\s\w+\s\w+',str((link.contents)[0])):
				continue
			if re.match(r'Только что',str((link.contents)[0])):
				continue
			if re.match(r'Предложить идею',str((link.contents)[0])):
				continue
			else:
				forum_links[link.getText()] = link.get('href')
	print(len(forum_links))
	return forum_links
	#l = list(filter(None, forum_links))
	#res = [x for x in l if re.search("id", x)]
	#print(res)
	#print(len(res))
	#return res

def main():
	topics = forum_checker(URL)
	print(topics)
#	for topic in topics[0:1]:
	#	extract_from_topic(topic)




if __name__ == "__main__":
	main()
