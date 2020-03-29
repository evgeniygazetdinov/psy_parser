#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict
from lib.one_table_func import find_likes, get_topic_id, find_quote_in_table, get_number_post,parse_one_table 

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


def all_pagination(current_number_page):
	#danger recursive_stuff
	return links

"""
#some realization
def funk(page):
	all_paginated = []
	all_links = some_work()
	all_paginated.append(all_links)
	if all_links =="следуюшая страница":
		all_paginated.append(funk(all_links[-1]))
	return all_links
"""


def find_pages_in_topic(soup):
	#Target find entity which go to link return all links if last link equlize == "SLEDUUSHAYA STRANITSA" do work again
	all_pages = []
	paginated = soup.find("div",{"class":"page-list"})
	current_number_page = paginated.find_all('a')
	#if last link is next page 
#	for page in current_number_page:
		#if re.match(r'Следующая страница',str((page.contents)[0])):



	




def check_pagination(topics,topic_name,topic_url):
	#change list_urls if url has pagination ==> add pagination link to list
	#to match tricky way
	#get older dict check paginate after push into new
	page = requests.get(HOST+topic_url[0])
	soup = BeautifulSoup(page.content,features="lxml")
	if soup.find("div",{"class":"page-list"}):
		topics[topic_name] = find_pages_in_topic(topic_url)

		#topics[topic_name].append()


def get_info_from_topic(topic):
	page = requests.get(HOST+topic)
	soup = BeautifulSoup(page.content,features="lxml")
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info


def main():
	topics = forum_checker(URL)
	topics_with_pagination = OrderedDict()
	for topic_name,topic_link in topics.items():
		print(topic_name)
		check_pagination(topics_with_pagination,topic_name,topic_link)
		#extract_from_topic(topic_link)




if __name__ == "__main__":
	main()
