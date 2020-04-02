from more_itertools import unique_everseen
import csv
with open('out.csv','r') as f, open('2.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))

with open('out.csv',newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=";")
    sortedlist = sorted(spamreader, key=lambda row:'topic_name', reverse=False)


with open('out2.csv', 'w') as f:
    fieldsis= ['topic_id','topic_name','number_message','timestamp','txt_msg','likes','quote','who']
    writer = csv.DictWriter(f, fieldnames=fieldsis)
    writer.writeheader()
    for row in sortedlist:
        writer.writerow(row)
