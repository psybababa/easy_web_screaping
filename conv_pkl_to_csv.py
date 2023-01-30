#dataフォルダに入っているpklをcsvに変換し、追記していく。こっちはファイル操作に関するメソッドが格納されていく。

import pandas as pd

class df_toolbox:
    def convcsv():
        df_threads = pd.read_pickle('./data/threads.pkl') 
<<<<<<< HEAD
        print(df_threads)
        df_threads.to_csv('./data/threads.csv',encoding='utf-8_sig',mode='a')
        
df_toolbox.convcsv
        
=======
        df_threads.to_csv('./data/threads.csv',encoding='utf-8_sig',mode='a',header=False)
        
df_toolbox.convcsv()
>>>>>>> 3f2c3a1983da8c48f59aa84d3cbb3e51e738062a
