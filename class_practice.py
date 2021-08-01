# coding:utf-8
# -*- coding: utf8 -*-

import MeCab
import unidic

import codecs
import re
#import csv
#import time
import pandas as pd
from statistics import mean
#import matplotlib.pyplot as plt
#import random
#import twitterAPI
import pn_dictionary

tagger = MeCab.Tagger("")

class second_paper(pn_dictionary.PN_dictionary):
    def get_diclist(self,sample_txt):
        self.result = tagger.parse(sample_txt)
        #print(result)
        lines = self.result.split('\n')
        lines =lines[0:-2]
        diclist = []
        for word in lines:
                l = re.split('\t|,',word)  # 各行はタブとカンマで区切られてるので
                #print(l)
                d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[11]}
                diclist.append(d)
        #print(diclist)
        diclist_new = []
        for word in diclist:
            self.base = word['BaseForm']
            print("基本形:"+self.base)        # 個々の辞書から基本形を取得
            if self.base in self.pn_dictA:
                pn = float(self.pn_dictA[self.base])  # 中身の型があれなので
            else:
                pn = 'notfound'            # その語がPN Tableになかった場合
            word['PN'] = pn
            diclist_new.append(word)
            #print(diclist_new)
        return(diclist_new)

sample_txt = input('形態素解析したい文章を入力してください:')
a = second_paper()
b = a.get_diclist(sample_txt)
print(b)

def get_pnmean(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        pnmean = mean(pn_list)
    else:
        pnmean = 0              # 全部notfoundならゼロにする
    print(pn_list)
    return(pnmean)

pnave = get_pnmean(b)
print(pnave)
