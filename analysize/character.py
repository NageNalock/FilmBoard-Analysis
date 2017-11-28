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
        self.elsecontents = []
        self.d = {}
        self.stopwords = ''
        self.num = 0
        self.elsenum = 0
        self.sum_key = {}
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
        f2 = open(abspath + '/test.txt', 'w+')
        for row in csv_f:
            if row[8].strip() == '-1':
                continue
            if row[1].strip().find('九寨') != -1 and row[1].find('地震') != -1:
                f = open(abspath + '/test2.txt', 'a+')
                f.write(row[1].strip() + '\n')
                f.close()
                l = {'flag':row[8], 'hang':row[0]}
                self.num = self.num + 1
                ss = jieba.cut(row[1].strip(), cut_all=False)
                for s in ss:
                    if self.stopwords.find(s) == -1 and l.get(s, -1) == -1:
                        l[s] = 0
                self.contents.append(l)
            else:
                l = {'flag': row[8], 'hang': row[0]}
                self.elsenum = self.elsenum + 1
                ss = jieba.cut(row[1].strip(), cut_all=False)
                for s in ss:
                    if self.stopwords.find(s) == -1 and l.get(s, -1) == -1:
                        l[s] = 0
                self.elsecontents.append(l)
                f2.write(row[8] + ':' + row[0] + '@' + row[1].strip() + '\n')
        f.close()
        f2.close()

    def set_tf(self):
        sum_key_A = {}
        sum_key_B = {}
        s1 = float(self.num) / (self.num + self.elsenum)
        s2 = float(self.elsenum) / (self.num + self.elsenum)
        s = 0 - s1 * math.log(s1) - s2 * math.log(s2)
        for content in self.contents:
            for key in content:
                if key == 'flag' or key == 'hang':
                    continue
                if sum_key_A.get(key, -1) == -1:
                    sum_key_A[key] = 1
                else:
                    sum_key_A[key] = sum_key_A[key] + 1

        for key in sum_key_A:
            sum_key_B[key] = 0
            for content2 in self.elsecontents:
                if content2.get(key, -1) != -1:
                    sum_key_B[key] = sum_key_B[key] + 1
            A = sum_key_A[key]
            B = sum_key_B[key]
            C = self.num - sum_key_A[key]
            D = self.elsenum - sum_key_B[key]
            pab = float(A + B) / (self.num + self.elsenum)
            pa = float(A) / (A + B)
            pb = float(B) / (A + B)
            pcd = float(C + D) / (self.num + self.elsenum)
            pc = float(C) / (C + D)
            pd = float(D) / (C + D)
            if pa == 0:
                sa = 0
            else:
                sa = pa*math.log(pa)
            if pb == 0:
                sb = 0
            else:
                sb = pb*math.log(pb)
            if pc == 0:
                sc = 0
            else:
                sc = pc*math.log(pc)
            if pd == 0:
                sd = 0
            else:
                sd = pd*math.log(pd)
            self.sum_key[key] = s + pab*(sa + sb) + pcd*(sc + sd)

        self.sum_key_sorted = sorted(self.sum_key.iteritems(), key=lambda asd: asd[1], reverse=True)

        f2 = open(abspath + '/shang.txt', 'w+')
        for key in self.sum_key_sorted:
            f2.write(key[0] + ':' + str(key[1]) + '\n')
        f2.close()

    def set_calculate(self):
        keys = {}
        count = 0
        for content in self.elsecontents:
            for key in content:
                if key == 'flag' or key == 'hang':
                    continue
                self.elsecontents[count][key] = self.sum_key.get(key, 0)
            count = count + 1
        count = 0
        fenmu2 = 0
        for key in self.sum_key_sorted:
            # if key[1] < 0.000001:
            #     break
            fenmu2 = fenmu2 + key[1] * key[1]
        for content in self.elsecontents:
            fenzi = 0
            fenmu1 = 0
            for key in content:
                if key == 'flag' or key == 'hang':
                    continue
                if self.sum_key.get(key, 0) >= 0.009:
                    fenzi = fenzi + content[key] * self.sum_key.get(key, 0)
                    fenmu1 = fenmu1 + content[key] * content[key]
            if fenmu1 == 0:
                self.elsecontents[count]['xiangsidu'] = 0
            else:
                fenmu = math.sqrt(fenmu1) * math.sqrt(fenmu2)
                self.elsecontents[count]['xiangsidu'] = fenzi / fenmu
            count = count + 1
        f = open(abspath + '/test.txt', 'r+')
        readlines = f.readlines()
        f.close()
        f2 = open(abspath + '/test2.txt', 'a+')
        count = 0
        self.counts = 0
        for readline in readlines:
            if self.elsecontents[count]['xiangsidu'] > 0.5:
                if self.elsecontents[count]['flag'] == '0':
                    self.counts = self.counts + 1
                f2.write(str(self.elsecontents[count]['xiangsidu']) + ' ' + readline)
            count = count + 1
        f2.close()



filepath = abspath + '/weibocsv'
files = os.listdir(filepath)

count = 0
for fileap in files:
    f = file(filepath+'/' + fileap)
    f.set_tf()
    f.set_calculate()
    count = count + f.counts

print count