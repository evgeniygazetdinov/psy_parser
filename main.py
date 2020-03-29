#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict
from lib.one_table_func import get_info_from_topic, find_likes, get_topic_id, find_quote_in_table, get_number_post,parse_one_table 
from lib.pagination import make_faked_links, get_links_from_link, find_nested_links, check_pagination, links_with_pagination  
import time 



URL = "https://www.b17.ru/forum/?f=102"
HOST = 'https://www.b17.ru'


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
				forum_links[link.getText()] = [link.get('href')]
	print(len(forum_links))
	return forum_links


def extract_from_topic(topic_link):
	info = get_info_from_topic(topic_link)
	#paginate here
	for info_for_write in info:
			parse_one_table(info_for_write)


def main():
	topics = forum_checker(URL)
	topics_with_pagination = links_with_pagination(topics)
	#extract info 
	print(topics_with_pagination)
	#write_it by line into file


if __name__ == "__main__":
	main()
