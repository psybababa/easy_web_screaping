#dataフォルダに入っているpklをcsvに変換し、追記していく。こっちはファイル操作に関するメソッドが格納されていく。
import os
import pandas as pd

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
    def delunnecessaryraw():
        fname = input('what is file name? ')
        
        if not os.path.exists('./data/{fname}.csv'):
            print(f'error happend while opening {fname}.csv')
            quit()
            
        rawdata = pd.read_csv(f'./data/{fname}.csv')
        rawdata.drop_duplicates(inplace = True,keep = 'first')
        cleaneddata = rawdata.dropna(how = 'any')
        cleaneddata.to_csv(f'./data/cleaned{fname}.csv',encoding = 'utf_8_sig',mode = 'a')
            