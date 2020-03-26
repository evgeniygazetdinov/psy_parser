#!/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

URL = "https://www.b17.ru/forum/?f=102"



def forum_checker(URL):
	#get all from one paginate page
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
	forum_checker(URL)
	print("this main")




if __name__ == "__main__":
	main()
