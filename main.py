from apscheduler.schedulers.blocking import BlockingScheduler
from df_toolbox import df_converter
from scrape_onj import scrape

sched = BlockingScheduler()

@sched.scheduled_job('interval',hours = 3)

def run_scraping():
    scrape.scan_threads()
    df_converter.convthreads()
    scrape.get_title_list()
    scrape.get_comments()
    df_converter.convtitles()
    df_converter.convcomments()
  
    
    
sched.start()