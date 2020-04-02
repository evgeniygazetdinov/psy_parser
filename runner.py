import time
import sys
from now import how_many_rows_now

while(how_many_rows_now() <20000000):
	try:
		exec(open('main.py').read())
		print('now rows')
		print(how_many_rows_now())
		time.sleep(5)
	except:
		print("something happend")
		print(sys.exc_info()[1])
		pass
