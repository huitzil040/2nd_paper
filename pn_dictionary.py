# coding:utf-8
# -*- coding: utf8 -*-

import unidic
import codecs
import re
import pandas as pd
from statistics import mean

class PN_dictionary():
    def __init__(self):
        self.pn_df = pd.read_csv('dictionary/JSPD/pn_2.csv',\
                        sep=':',
                        encoding='utf-8',
                        names=('Word','PN')
                       )
        self.pn_df_2 = pd.read_csv('dictionary/JSPD/wago_2.csv',\
                        sep=':',
                        encoding='utf-8',
                        names=('PN','Word')
                       )
        self.word_list = list(self.pn_df['Word'])
        self.pn_list = list(self.pn_df['PN'])  # 中身の型はnumpy.float64
        self.word_list2 = list(self.pn_df_2['Word'])
        self.pn_list2 = list(self.pn_df_2['PN'])
        self.pn_dict = dict(zip(self.word_list, self.pn_list))
        self.pn_dict2 = dict(zip(self.word_list2, self.pn_list2))
        self.pn_dict.update(self.pn_dict2)

        with codecs.open("dictionary/pn_ja.dic.txt", "r", "Shift-JIS", "ignore") as file:
            self.pn_dfA = pd.read_csv(file,\
                                sep=':',
                                encoding='utf-8',
                                names=('Word','Reading','POS', 'PN')
                               )
        #print(pn_df)
        self.word_listA = list(self.pn_dfA['Word'])
        self.pn_listA = list(self.pn_dfA['PN'])  # 中身の型はnumpy.float64
        self.pn_dictA = dict(zip(self.word_listA, self.pn_listA))
