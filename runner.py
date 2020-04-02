import time
import sys

def how_many_rows_now():
	with open('out.csv') as f:
    	   return sum(1 for line in f)	


while(how_many_rows() <20000000):
    try:
        exec(open('main.py').read())
	print('now rows ')
	print(how_many_rows_now())
        time.sleep(5)
    except:
        print("something happend")
        print(sys.exc_info())
        pass
