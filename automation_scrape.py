#四時間ごとにスクレイピングからcsvまでの保存を行う。

import conv_pkl_to_csv as cpc
import schedule
import time
import open_2ch_scraping as o2s
import os


def job():
   o2s.scrape_onj.parse_thread()
   cpc.df_toolbox.convcsv()
   os..remove('./data/threads.pkl')

schedule.every(4).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
