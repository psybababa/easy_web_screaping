#dataフォルダに入っているpklをcsvに変換し、追記していく。こっちはファイル操作に関するメソッドが格納されていく。

import pandas as pd

class dfconvert:
    def convcomments():
        with open('./data/comments.pkl') as df: 
            df.to_csv('./data/comments.csv',encoding='utf-8_sig',mode='a')
        
    def convthreads():
        with open('./data/threads.pkl') as df:        
            df.to_csv('./data/threads.csv',encoding='utf-8_sig',mode='a')
        
    def convtitles():
        with open('./data/titles.pkl') as df:
            df.to_csv('./data/titles.csv',encoding='utf-8_sig',mode='a')


class  dfprocessing: