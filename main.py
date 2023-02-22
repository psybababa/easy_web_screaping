from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time
from df_toolbox import dfconvert
from scrapeonj import scrape


sched = BlockingScheduler()

@sched.scheduled_job('interval',hours = 6)

def runscraping():
    scrape.scanthreads()
    print('Scanned threads')
    scrape.gettitlelist()
    print('Collected titles')
    scrape.getcomments()
    print('scraped all comments')
    
def converttocsv():
    dfconvert.convthreads()
    dfconvert.convtitles()
    dfconvert.convcomments()
    print('All converted')
  
  
sched.add_job(runscraping, 'interval', hours = 6)
sched.add_job(converttocsv, 'interval', hours = 6)   
    
sched.start()