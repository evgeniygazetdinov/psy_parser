import re
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer 
from lib.const import URL, HOST, DELAY, headers, write_to_csv
import datetime
from collections import OrderedDict

def get_topic_id(from_topic):
	raw_topic = re.findall(r'\w{2}=\S\w{4}_\d+',str(from_topic))
	if raw_topic:
		topic_id = raw_topic[0].split('id="post_')
		return topic_id[1]
	return 		

def find_quote_in_table(soup):
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
	# remove spaces 
	template = str(raw_date).strip()
	if re.match(r'Сегодня',template):
		print('HERER')
		raw_date_formating = raw_date.split('-')
		extact_hour_minute = (raw_date_formating[-1]).split(':')
		hour,minute = extact_hour_minute[0],extact_hour_minute[1]
		return str(hour+minute)
		# time_place = date = datetime.strptime(now,' %d %b %Y')
		# newdates = date.replace(hour=11, minute=59)
		# print(newdate)
	if re.match(r'Вчера', template):
		print('HERER')
		raw_date_formating = raw_date.split('-')
		extact_hour_minute = (raw_date_formating[-1]).split(':')
		hour,minute = extact_hour_minute[0],extact_hour_minute[1]
		return str(hour+minute)
	return raw_date


def insert_time_stamp(soup):
	clear_date = datetime.datetime.now()
	try:
		results = soup.find('p', attrs={"class":"date"})
		clear_date = ((results.text).split('|'))[-1]
		vchera_to_date = convert_to_date(clear_date)
	except:
		pass
		return clear_date

def get_number_post(soup):
	results = soup.find('p', attrs={"class":"date"})
	clear_number= ((results.text).split('|'))[0]
	number = (clear_number.split('№'))[-1]
	return number
#
def get_info_from_topic(topic):
	page = requests.get(HOST+topic, headers=headers,)
	soup = BeautifulSoup(page.content,features="lxml")
	time.sleep(DELAY)
	topic_info = soup.find_all("table",{"class":"topic_post"})
	return topic_info


def parse_one_table(topic_name,table):
	info_for_write = OrderedDict()
	soup = BeautifulSoup(str(table),"lxml")
	#extract values
	#rebuild regexp
	info_for_write['topic_id'] = get_topic_id(table)
	print(info_for_write['topic_id'])
	info_for_write['topic_name'] = topic_name
	print(info_for_write['topic_name'])
	#TODO
	info_for_write['number_message'] = get_number_post(soup)

	info_for_write['likes']  = find_likes(soup)
	print(info_for_write['likes'])

	#TODO
	info_for_write['timestamp'] = insert_time_stamp(soup)

	print(info_for_write['timestamp'])
	info_for_write['txt_msg'] = find_text_message(soup)
	print(info_for_write['txt_msg'])
	info_for_write['quote'] = find_quote_in_table(soup)
	print(info_for_write['quote'])
	info_for_write['who']  = find_author(soup)
	print(info_for_write['who'])
	write_to_csv(info_for_write)
