#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
from collections import OrderedDict

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
	for info_for_write in info:
			parse_one_table(info_for_write)

def get_topic_id(from_topic):
	raw_topic = re.findall(r'\w{2}=\S\w{4}_\d+',str(from_topic))
	if raw_topic:
		topic_id = raw_topic[0].split('id="post_')
		return topic_id[1]
	return 		

def find_quote_in_table(table):
	results = soup.find('div', attrs={"class":"quote"})
	if results:	
		quote = (((((results.text).split('писал(а)')[-1]).split(':'))[-1]))
		if not quote:
			return 'no'
		else:
			return quote
	return 'no'

def find_author(soup):
	
	results = soup.find('td', attrs={"class":"mes qq"})
	clear_author = ((results['fio']).split('|'))[-1]
	return clear_author
	
def find_text_message(soup):
	results = soup.find('td', attrs={"class":"mes qq"})
	return results.text
	

def find_likes(soup):
	results = soup.find('span', attrs={"class":"n"})
	if results:
		return str(results.text)
	return '0'


def convert_to_date(raw_date):
	now = datetime.datetime.now()
	if re.match(r'Сегодня',str(raw_date)):
		raw_date_formating = raw_date.split('-')
		extact_hour_minute = (raw_date_formating[-1]).split(':')
		hour,minute = extact_hour_minute[0],extact_hour_minute[1]
		return hour+minute
		# time_place = date = datetime.strptime(now,' %d %b %Y')
		# newdates = date.replace(hour=11, minute=59)
		# print(newdate)
	else:
		if re.match(r'Вчера',str(raw_date)):
			raw_date_formating = raw_date.split('-')
			extact_hour_minute = (raw_date_formating[-1]).split(':')
			hour,minute = extact_hour_minute[0],extact_hour_minute[1]
			return hour+minute
		else:
			return raw_date
	




def insert_time_stamp(soup):
	try:
		results = soup.find('p', attrs={"class":"date"})
		clear_date = ((results.text).split('|'))[-1]
		#vchera_to_date = convert_to_date(clear_date)
		return clear_date
	except:
		pass

def get_number_post(soup):
	pass
def parse_one_table(table):
	soup = BeautifulSoup(str(table),"lxml")
	#extract values
	#rebuild regexp
	# topic_id = get_topic_id(table)
	# quote = find_quote_in_table(table)
	# print(quote)
	# print(topic_id)
	# author = find_author(soup,table)
	# print(author)	
	likes = find_likes(soup)
	print(likes)
	date = insert_time_stamp(soup)
	print(date)
def get_info_from_topic(topic):
	page = requests.get(HOST+topic)
	soup = BeautifulSoup(page.content,features="lxml")
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info


def main():
	topics = forum_checker(URL)
	for topic_name,topic_link in topics.items():
		print(topic_name)
		extract_from_topic(topic_link)




if __name__ == "__main__":
	main()
