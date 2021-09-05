# coding:utf-8
# -*- coding: utf8 -*-

import MeCab
import unidic
import os
import csv
import codecs
from statistics import mean
import re
import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np
import twitterAPI
import pn_dictionary
import tweepy

pnmeans_list = []

tagger = MeCab.Tagger("")

def get_pnmean(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        pnmean = mean(pn_list)
    else:
        #pnmean = "notfound"            # 全部notfoundならゼロにする
        pnmean = 0
        #break
    #print(pn_list)
    return(pnmean)


class tweet_collect():
    def search(search_word):
        result_list = []
        #search_results = twitterAPI.api.search(search_word)
        dict_type = "i"
        for tweet in tweepy.Cursor(twitterAPI.api.search, q=search_word,tweet_mode='extended',lang='ja').items(500):
            #print(tweet.text)
            #print("="*80)
        for i in range(len(result_list)):
            result_list[i] = result_list[i].replace('\n', ' ')

        for tw in result_list:
            a = second_paper()
            dl_old = a.get_diclist(tw, dict_type)
            #print(dl_old)
            pnmean = get_pnmean(dl_old)
            #print(pnmean)
            pnmeans_list.append(pnmean)
        #print(pnmeans_list)
        aura_df = pd.DataFrame({'text':result_list,'PN':pnmeans_list,},
                               columns=['text', 'PN']
                              )

        aura_df = aura_df.sort_values(by='PN', ascending=True)
        aura_df.to_csv('aura.csv',\
                        index=None,\
                        encoding='utf-8',\
                        quoting=csv.QUOTE_NONNUMERIC\
                       )
        return(result_list)

class second_paper(pn_dictionary.PN_dictionary):
    def get_diclist(self,sample_txt,dict_type):
        self.result = tagger.parse(sample_txt)
        #print(result)
        lines = self.result.split('\n')
        lines =lines[0:-2]
        #print(lines)
        diclist = []
        for word in lines:
                l = re.split('\t|,',word)  # 各行はタブとカンマで区切られてるので
                #print(l)
                if len(l) > 8:
                    d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[11]}
                    diclist.append(d)
                else:
                    print("Error:"+l[0])
        #print(diclist)
        diclist_new = []
        for word in diclist:
            self.base = word['BaseForm']
            print("基本形:"+self.base)        # 個々の辞書から基本形を取得
            if dict_type == "t":
                if self.base in self.pn_dictA:
                    pn = float(self.pn_dictA[self.base])  # 中身の型があれなので
                else:
                    pn = 'notfound'            # その語がPN Tableになかった場合
            elif dict_type == "i":
                if self.base in self.pn_dict:
                    pn = float(self.pn_dict[self.base])  # 中身の型があれなので
                else:
                    pn = 'notfound'            # その語がPN Tableになかった場合
            word['PN'] = pn
            diclist_new.append(word)
            #print(diclist_new)
        return(diclist_new)

class mord_changer():
    def twitter_search():
        search_word = input('検索したい単語を入力してください:')
        text_list = tweet_collect.search(search_word)
        #print(text_list)

    def word_mecab():
        sample_txt = input('形態素解析したい文章を入力してください:')
        a = second_paper()
        dict_type = input("分析に用いる辞書を選んでください(t/i)")
        if (dict_type == "t") or (dict_type == "i"):
            b = a.get_diclist(sample_txt,dict_type)
            pnave = get_pnmean(b)
            if pnave == "notfound":
                pnave = 0
            print("結果"+"-"*50)
            print(pnave)
        else:
            print("t or i !!!!!!!!!!!!!!!")


mord = input('使用する機能を選択してください(t/w):')
if mord == "t":
    mord_changer.twitter_search()
elif mord == "w":
    b = mord_changer.word_mecab()
else:
    print("t or w !!!!!!!!!!!!!!!")
    b = "間違ってるよ！"


#pnave = get_pnmean(b)
#print("結果"+"-"*50)
#print(pnave)
