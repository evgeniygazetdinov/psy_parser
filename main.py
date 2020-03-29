#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict
from lib.one_table_func import find_likes, get_topic_id, find_quote_in_table, get_number_post,parse_one_table 
import time 
from lib.change_ip import changer


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


def all_numbers_in_page(url):
	page = requests.get(HOST+url[0])
	soup = BeautifulSoup(page.content,features="lxml")
	paginated = soup.find("div",{"class":"page-list"})
	all_links_in_current_page = paginated.find_all('a')
	return all_links_in_current_page

"""
#some realization
def funk(page):
	all_paginated = []
	#return links from page
	all_links = some_work()
	all_paginated.append(all_links)
	if all_links =="следуюшая страница":
		all_paginated.append(funk(all_links[-1]))
	return all_paginated
"""


def find_pages_in_topic(link):
	#Target find entity which go to link return all links if last link equlize == "SLEDUUSHAYA STRANITSA" do work again
	all_pages = []
	all_links = all_numbers_in_page(link)
	if re.match(r'Следующая страница',str(((all_links[-1]).contents)[0])):
		all_pages.append(find_pages_in_topic(all_links[-1].get('href')))
	return all_pages
	#if last link is next page 
#	for page in current_number_page:
		#if re.match(r'Следующая страница',str((page.contents)[0])):

def some_functional(topic_url):
	links = []
	res = []
	page = requests.get(HOST+topic_url)
	soup = BeautifulSoup(page.content,features="lxml")
	if soup.find("div",{"class":"page-list"}):
		f = soup.find("div",{"class":"page-list"})
		a = f.find_all('a')
		if re.match(r'Следующая страница',str(((a[-1]).contents)[0])):
			print((a[-1]).get('href'))
			some_functional((a[-1]).get('href'))
			print('in recursive')
			time.sleep(.700)
			res.append((a[-1]).get('href'))
		for i in a:
			res.append((i).get('href'))
		return res
	return [topic_url]



def check_pagination(topics,topic_name,topic_url):
	#change list_urls if url has pagination ==> add pagination link to list
	#to match tricky way
	#get older dict check paginate after push into new
	topic_links = some_functional(topic_url[0])
	print('this result in topic')
	print(topic_links)
	print('^'*10)
		#topics[topic_name] = find_pages_in_topic(topic_url)

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
		#fuck void func
		check_pagination(topics_with_pagination,topic_name,topic_link)
		#extract_from_topic(topic_link)
	#changer()


if __name__ == "__main__":
	main()
