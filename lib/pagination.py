from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import time 
from lib.const import HOST, DELAY, headers
import re


def make_faked_links(host, number):
	links = []
	for i in range(1,number+1,1):
		links.append(str('/forum/'+host+'p='+str(i)+'#topic_top'))
	return links

def get_links_from_link(link):
	parse_link = link.split('p=')
	host = parse_link[0]
	clean_number = parse_link[-1].split('#')
	links = make_faked_links(host,int(clean_number[0]))
	return links


def find_nested_links(topic_url):
	#if he exist
	links = []
	page = requests.get(HOST+topic_url,headers=headers)
	soup = BeautifulSoup(page.content,features="lxml")
	time.sleep(DELAY)
	if soup.find("div",{"class":"page-list"}):
		f = soup.find("div",{"class":"page-list"})
		a = f.find_all('a')
		links = get_links_from_link(a[-2].get('href'))
		return links
	return [topic_url]


def check_pagination(topic_url):
	topic_links = find_nested_links(topic_url[0])
	return topic_links


def links_with_pagination(topics):
	topics_with_pagination = OrderedDict()
	for topic_name,topic_link in topics.items():
		topics_with_pagination[topic_name] = check_pagination(topic_link)
	return topics_with_pagination
