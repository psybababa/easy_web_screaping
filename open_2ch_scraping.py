#製作途中

from bs4 import BeautifulSoup as bs
import cloudscraper
import pandas as pd
import re
import time

class scrape_onj:
    scraper = cloudscraper.create_scraper(delay=1, browser="chrome") #cloudflareサーバーの1020エラーによるブロックを防ぐためrequestsではなくcloudscraperを用いる。尚、おーぷん2chではプロクシは使用できない。
        
    def get_links():
    #スクレイピング作業をまずはおんJのスレッド一覧で行い、リンクを手に入れる。
     links = list()
     html_ti = scrape_onj.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
     soup_ti = bs(html_ti.content,"html.parser")
     tags = soup_ti('a')
     for tag in tags:
             links.append(tag.get('href',None))
     return links

     def parse_thread():
        df_list = list()
        temp_dict = dict()
        links = scrape_onj.get_links()
        for link in links:
                if len(link) < 2:
                        continue
                r = scrape_onj.scraper.get(link)
                soup = bs(r.content,'html.parser')
                main_wrap = soup(class_ ='MAIN_WRAP')
                for tag in main_wrap:
                        temp_dict['title'] = soup.h1.text
                        temp_dict['comments'] = soup.dl.dd.text
                        icchidatas = soup.dl.dt.text
                        nanashi = re.findall('1 ：(...)',icchidatas)
                        date = re.findall(r'\d*/\d*/\d*',icchidatas)
                        timetable= re.findall(r'\d*:\d*:\d*',icchidatas)
                        id = re.findall('ID:(....)',icchidatas)
                        temp_dict['nanashi'] = nanashi[0]
                        temp_dict['date'] = date[0]
                        temp_dict['timetable'] = timetable[0]
                        temp_dict['id'] = id[0]
                df_list.append(temp_dict)
                temp_dict = {}
                
        time.sleep(1)
                
        thereads_df = pd.DataFrame(df_list)
        thereads_df.to_csv("./threads.csv",encoding='utf-8_sig',mode='a')
        
scrape_onj.parse_thread()
