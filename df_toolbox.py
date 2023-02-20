#dataフォルダに入っているpklをcsvに変換し、追記していく。こっちはファイル操作に関するメソッドが格納されていく。

import pandas as pd

class df_converter:
    def convcomments():
        df_threads = pd.read_pickle('./data/comments.pkl') 
        df_threads.to_csv('./data/comments.csv',encoding='utf-8_sig',mode='a')
        
    def convthreads():
        df_threads = pd.read_pickle('./data/threads.pkl') 
        df_threads.to_csv('./data/threads.csv',encoding='utf-8_sig',mode='a')
        
    def convtitles():
        df_threads = pd.read_pickle('./data/titles.pkl') 
        df_threads.to_csv('./data/titles.csv',encoding='utf-8_sig',mode='a')

df_converter.convcomments()