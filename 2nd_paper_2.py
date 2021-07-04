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


pn_df = pd.read_csv('dictionary/JSPD/pn_2.csv',\
                sep=':',
                encoding='utf-8',
                names=('Word','PN')
               )

print(pn_df)
print(pn_df.isnull())
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])  # 中身の型はnumpy.float64
pn_dict = dict(zip(word_list, pn_list))
#print(pn_dict)

def add_pnvalue(diclist_old):
    diclist_new = []
    for word in diclist_old:
        base = word['BaseForm']
        print(base)        # 個々の辞書から基本形を取得
        if base in pn_dict:
            pn = float(pn_dict[base])  # 中身の型があれなので
        else:
            pn = 'notfound'            # その語がPN Tableになかった場合
        word['PN'] = pn
        diclist_new.append(word)
    return(diclist_new)

tagger = MeCab.Tagger()  # 「tagger = MeCab.Tagger('-d ' + unidic.DICDIR)」

sample_txt = input('形態素解析したい文章を入力してください:')
def get_diclist(text):
    result = tagger.parse(sample_txt)
    print(result)
    lines = result.split('\n')
    lines =lines[0:-2]
    diclist = []
    for word in lines:
            l = re.split('\t|,',word)  # 各行はタブとカンマで区切られてるので
            d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[9]}
            diclist.append(d)
    return(diclist)

ans = get_diclist(sample_txt)
print(ans)
val = add_pnvalue(ans)
print(val)

# 各ツイートのPN平均値をとる関数
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
    return(pnmean)

pnave = get_pnmean(val)
print(pnave)
