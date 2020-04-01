#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict
from lib.one_table_func import get_info_from_topic, find_likes, get_topic_id, find_quote_in_table, get_number_post, parse_one_table 
from lib.pagination import make_faked_links, get_links_from_link, find_nested_links, check_pagination, links_with_pagination  
from lib.const import URL, HOST, DELAY, headers, write_to_csv
from lib.protect import do_some_protection
import time 



def forum_checker(URL):
	#get all from one paginate pagegit
	forum_links = OrderedDict()
	page = requests.get(URL, headers = headers)
	time.sleep(DELAY)
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


def extract_from_topic(topic_dict):
	for topic_name,topic_links in topic_dict.items():
		for topic_link in topic_links:
			info = get_info_from_topic(topic_link)
			for info_for_write in info:
				if len(info_for_write) == 0:
					continue
				parse_one_table(topic_name, info_for_write)


def main():
	#for avoid
	do_some_protection()
	
	topics = forum_checker(URL)
	topics_with_pagination = links_with_pagination(topics)
	extract_info = extract_from_topic(topics_with_pagination)


if __name__ == "__main__":
	main()