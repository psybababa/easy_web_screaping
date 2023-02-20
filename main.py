from apscheduler.schedulers.blocking import BlockingScheduler
from df_toolbox import df_toolbox
from scrape_onj import scrape_onj

sched = BlockingScheduler()

@sched.scheduled_job('interval',hours = 3)

def run_scraping():
    scrape_onj.scan_threads()
    df_toolbox.convthreads()
    scrape_onj.get_comments()
    df_toolbox.convtitles()
    df_toolbox.convcomments()
  
    
    
sched.start()