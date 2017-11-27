import os
abspath = os.path.abspath('.')
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf-8')

files = os.listdir(abspath + '/weibocsv')

f2 = open('test3.txt', 'w+')

for file in files:
    f = open(abspath + '/weibocsv/' + file, 'r+')
    reader = csv.reader(f)
    for row in reader:
        if row[8] == '1':
            f2.write(row[1].strip() + '\n')
    f.close()

f2.close()