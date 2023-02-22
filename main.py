from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time
from df_toolbox import dfconvert
from scrapeonj import scrape


sched = BackgroundScheduler()

@sched.scheduled_job('interval',hours = 6)

def runscraping():
    scrape.scanthreads()
    scrape.gettitlelist()
    scrape.getcomments()
    
    dfconvert.convthreads()
    dfconvert.convtitles()
    dfconvert.convcomments()
  
  
sched.add_job(runscraping, 'interval', hours = 6) 
    
sched.start()