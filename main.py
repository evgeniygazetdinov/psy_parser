#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict
from lib.one_table import 

URL = "https://www.b17.ru/forum/?f=102"
HOST = 'https://www.b17.ru'

def one_paginate():
	pass

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


def extract_from_topic(topic_link):
	info = get_info_from_topic(topic_link)
	print(topic_link)
	for info_for_write in info:
			parse_one_table(info_for_write)

def get_topic_id(from_topic):
	raw_topic = re.findall(r'\w{2}=\S\w{4}_\d+',str(from_topic))
	if raw_topic:
		topic_id = raw_topic[0].split('id="post_')
		return topic_id[1]
	return 		

def find_quote_in_table(table):
	pass

def find_author(table):
	pass

def find_likes(table):
	pass

def insert_time_stamp(table):
	pass

def parse_one_table(table):
	#extract values
	#rebuild regexp
	topic_id = get_topic_id(table)
	quote = find_quote_in_table(table)
	print(topic_id)	
	
def get_info_from_topic(topic):
	page = requests.get(HOST+topic)
	soup = BeautifulSoup(page.content,features="lxml")
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info


def main():
	topics = forum_checker(URL)
	for topic_name,topic_link in topics.items():
		extract_from_topic(topic_link)




if __name__ == "__main__":
	main()
