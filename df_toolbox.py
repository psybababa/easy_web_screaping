#こっちはデータの前処理がメイン。
import MeCab
import neologdn
import numpy
import os
import pandas as pd
import re
import spacy
from spacymoji import Emoji
import string


class dfconvert:
    def convcomments():
        df = pd.read_pickle('./data/comments.pkl')
        df.to_csv('./data/comments.csv',encoding='utf-8_sig',mode='a')
        
    def convthreads():
        df = pd.read_pickle('./data/threads.pkl')     
        df.to_csv('./data/threads.csv',encoding='utf-8_sig',mode='a')
        
    def convtitles():
        df = pd.read_pickle('./data/titles.pkl')
        df.to_csv('./data/titles.csv',encoding='utf-8_sig',mode='a')


class  dfpreprocess:
    #時間帯によってはスレが重複するので、それを削除する。
    def removeemptyraw():
        fname = input('what is file name? ')
        
        if not os.path.exists('./data/{fname}.csv'):
            print(f'error happend while opening {fname}.csv')
            quit()
            
        rawdata = pd.read_csv(f'./data/{fname}.csv')
        rawdata.drop_duplicates(inplace = True,keep = 'first')
        cleaneddata = rawdata.dropna(how = 'any')
        cleaneddata.to_csv(f'./data/cleaned{fname}.csv',encoding = 'utf_8_sig')
    
    #titleとcommentを正規化する。
    def normalizetext():
        fname = input('What is file name? ')
        
        if not os.path.exists('./data/cleaned{fname}.csv'):
            print(f'please enter cleaned file name {fname} Maybe {fname} is not cleaned yet or does not exist')
            quit()
            
        df = pd.read_csv(f'./data/cleaned{fname}.csv')
        df['title'] = df['title'].apply(neologdn.normalize)
        df['comment'] = df['comment'].apply(neologdn.normalize)
        df.to_csv(f'./data/normalized{fname}.csv')
            
        
    #好ましくないレスをフィルターにかける。
    def filterwords():
        with open('ignoredwords.txt') as iwf:
            ignoredwords = iwf.read().split(',')
        
        fname = input('what is file name?')
        
        if not os.path.exists(f'./data/normalized{fname}.csv'):
            print(f'error happend while opening{fname}.csv. Maybe {fname} is not normalized yet or does not exists')
            quit()
            
        df = pd.read_csv(f'./data/normalized{fname}.csv')
       
        #ここまでかいた。次はfilterwordsを決める為に、使われた数が多い言葉の中から不適切なものを選んでいく。mecabを使って分けた後にdicとgetを使う？。