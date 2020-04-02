# -*- coding: utf-8 -*-
import csv

tests={'German': [u'Straße',u'auslösen',u'zerstören'], 
       'French': [u'français',u'américaine',u'épais'], 
       'Chinese': [u'中國的',u'英語',u'美國人']}

with open('n.csv','w') as fout:
    writer=csv.writer(fout)    
    writer.writerows([tests.keys()])
    for row in zip(*tests.values()):
        row=[s.encode('utf-8') for s in row]
        writer.writerows([row])

