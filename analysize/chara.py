#-*- coding=utf-8 -*-
import jieba
import csv
import string
import math
import os
abspath = os.path.abspath('.')
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class file:
    def __init__(self, filepath):
        self.filepath = filepath
        self.contents = []
        self.d = {}
        self.stopwords = ''
        self.num = 0
        self.set()

    @property
    def filepath(self):
        return self.filepath

    @filepath.setter
    def filepath(self, value):
        self.filepath = value

    @property
    def key(self):
        return self.key

    __slots__ = {'filepath', 'key'}

    def set_stopwords(self):
        f = open(abspath + '/stopwords.txt', 'r+')
        readlines = f.readlines()
        for readline in readlines:
            self.stopwords = self.stopwords + readline[0:len(readline) - 1]
        f.close()

    def set(self):
        f = open(self.filepath, 'r+')
        csv_f = csv.reader(f)
        self.set_stopwords()
        for row in csv_f:
            if row[1].strip().find('九寨') != -1 and row[1].find('地震') != -1 and row[8].strip() != '-1':
                l = {'flag':row[8], 'hang':row[0]}
                self.num = self.num + 1
                ss = jieba.cut(row[1].strip(), cut_all=False)
                for s in ss:
                    if self.stopwords.find(s) == -1 and l.get(s, -1) == -1:
                        l[s] = 1
                self.contents.append(l)
        f.close()

        sum_key = {}
        for content in self.contents:
            for key in content:
                if key == 'flag' or key == 'hang':
                    continue
                if sum_key.get(key, -1) == -1:
                    sum_key[key] = 1
                else:
                    sum_key[key] = sum_key[key] + 1

        for key in sum_key:
            if key == '地震':
                print sum_key[key]
            sum_key[key] = 0 - float(sum_key[key])/self.num * math.log(float(sum_key[key])/self.num)

        sum_key = sorted(sum_key.iteritems(), key=lambda asd: asd[1], reverse=True)

        f2 = open(abspath + '/shang.txt', 'w+')
        for key in sum_key:
            f2.write(key[0] + ':' + str(key[1]) + '\n')
        f2.close()




f = file(abspath+'/weibocsv/1.csv')





