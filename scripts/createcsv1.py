import sys
import csv
import os
import sqlite3
con = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'brental1'))

cur = con.cursor()
cur.execute('SELECT * FROM traffic;')
rows = cur.fetchall()
fp = open(os.path.join(os.path.dirname(__file__), '..', 'data', 'traffic1.csv'), 'w')
myFile = csv.writer(fp)
myFile.writerows(rows)
fp.close()
print('traffic1.csv file successfully created')
con.commit()

