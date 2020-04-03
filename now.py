#!/usr/bin/env python
 # -*- coding: utf-8 -*-
def how_many_rows_now():
	with open('out.csv') as f:
    	   return sum(1 for line in f)	
print(how_many_rows_now())
