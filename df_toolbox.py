from collections import Counter as ct
from datetime import date
import numpy as np
import pandas as pd
import string
import sudachipy as sp

class Convert:
    def __init__(self):
        self.files = [
            {
                "fname": "comments",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {
                "fname": "threads",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {"fname": "titles",
             "encoding": "utf_8_sig",
             "mode": "a"
            },
        ]

    def convfile(self, finfo):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        df.to_csv(f"./data/{finfo['fname']}.csv", encoding=finfo["encoding"], mode=finfo["mode"])

    def convall(self):
        for finfo in self.files:
            self.convfile(finfo)

class process:
    dparam = {
        'date': date.today(), #日付を単位での検索用
        'time':None,#時間単位での検索用
        'id':None, #追跡したい特定のidがいればここに入力
        'num':None, #調べたいデータの数を入力すればよし
        'thread':None, #特定のスレッド内で検索したければここにurlを入力すればいいです
        }
        
    def changeparam(self):
        if self.param:
            self.dparam.update(self.param)
    
    def cleanfile(self, finfo):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        df['comment'] = df['comment'].replace('\n',' ')
        df['comment'] = df['comment'].translate(str.maketrans('','',string.punctuation))
        df['date'] = df['date'].replace('/','-')
        date_str = f"{df['date']}{df['timetable']}"
        df.drop(['date','timetable'],axis=1,inplace=True)
        df['datetime'] = pd.to_datetime(date_str)
        df.dropna(inplace=True, subset=['title', 'link'])
        df.drop_duplicates(subset='title', inplace=True)
        df = df.reindex(columns = ['comment','datetime','id','title','link'])
        df.to_pickle(f"./data/{finfo['fname']}_clean.pkl")
    
    def tokenize(self,txt):
        mode = sp.Tokenizer.SplitMode.B
        tokenizer = sp.Dictionary().create(mode)
        tokenizer.set_option("emoji", True)                
        tokens = tokenizer.tokenize(txt)
        return [t.surface() for t in tokens]
    
    def countid(self,finfo,n):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        cid = ct(df['id'])
        mcid = cid.most_common(n)
        return mcid
    
    def countwords(self,finfo,n):
        df = pd.read_pickle(f"./data/{finfo['word']}.pkl")
        cwds = ct(df['word'])
        mcwds = cwds.most_common(n)
        return mcwds
    
    def purseid(self,finfo,id,date):
        df = pd.read_pickle(f"./data/{finfo['word']}.pkl")
        idf = df[df['datetime'].day == date & df['ID'] == id ]
        return idf
    
class visualize:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    