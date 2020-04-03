from more_itertools import unique_everseen
import csv
with open('out.csv','r') as f, open('2.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))

