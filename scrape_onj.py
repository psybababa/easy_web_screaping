from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time

class scrape_onj:

    scraper = cloudscraper.create_scraper(delay=1, browser="chrome") #cloudflareサーバーの1020エラーによるブロックを防ぐためrequestsではなくcloudscraperを用いる。尚、おーぷん2chではプロクシは使用できない。
        
    def get_urls():
    #スクレイピング作業をまずはおんJのスレッド一覧で行い、リンクを手に入れる。
        urls = list()
        html_ll = scrape_onj.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
        soup_ll = bs(html_ll.content,'html.parser')
        tags = soup_ll('a')
        for tag in tags:
             urls.append(tag.get('href',None))
        return urls

    def scan_threads():
        df_lst = list()
        temp_dict = dict()
        urls =scrape_onj.get_urls()
        for url in urls:
                if len(url) < 2:
                        continue
                r = scrape_onj.scraper.get(url)
                soup = bs(r.content,'html.parser')
                main_wrap = soup(class_ ='MAIN_WRAP')
                for tag in main_wrap:
                        temp_dict['title'] = soup.h1.text
                        temp_dict['comments'] = (soup.dl.dd.text).strip()
                        icchidatas = soup.dl.dt.text
                        nanashi = re.findall('1 ：(...)',icchidatas)
                        date = re.findall(r'\d*/\d*/\d*',icchidatas)
                        timetable= re.findall(r'\d*:\d*:\d*',icchidatas)
                        id = re.findall('ID:(....)',icchidatas)
                        temp_dict['nanashi'] = nanashi[0]
                        temp_dict['date'] = date[0]
                        temp_dict['timetable'] = timetable[0]
                        temp_dict['id'] = id[0]
                df_lst.append(temp_dict)
                temp_dict.clear()
        time.sleep(1)
                
        threads_df = pd.DataFrame(df_lst)
        try:
                threads_df.to_pickle('./data/threads.pkl')
        except:
                os.mkdir('./data')
                threads_df.to_pickle('./data/threads.pkl')
                
    def get_title_list():  
        links = scrape_onj.get_urls()
        titles_lst = list()
        temp_dict = dict()
        for link in links:
               if len(link) < 2:
                       continue
               r = scrape_onj.scraper.get(link)
               soup = bs(r.content,'html.parser')
               main_wrap = soup(class_ ='MAIN_WRAP')
               for tag in main_wrap:
                       temp_dict = {}
                       temp_dict['title'] = soup.h1.text
                       temp_dict['link'] = link
                       titles_lst.append(temp_dict)
        temp_dict.clear()
        time.sleep(1)
        
        titles_df = pd.DataFrame(titles_lst)
        try:
                titles_df.to_pickle('./data/titles.pkl')
        except:
                os.mkdir('./data')
                titles_df.to_picke('./data/titles.pkl')
                
                
    def get_comments():
        scrape_onj.get_title_list()
        dlst = list()
        df_source = list()
        df = pd.read_pickle('./data/titles.pkl')
        df = df.loc[1:,['title','link']]
        for idx in zip(df['title'],df['link']):
                dlst.append(idx)
        for tp in dlst:
                source = scrape_onj.scraper.get(tp[1])
                soup = bs(source.content,'html.parser')
                val_tags = soup.find_all(class_ = re.compile('mesg hd'),attrs={'body','value'})
                temp_lst = list()
                for v_tag in val_tags:
                        temp_dict = dict()
                        comment = v_tag.dd.text
                        if re.search('!AA',comment) or re.search('imgur',comment):
                                continue
                        timetable = re.findall(r'\d*:\d*:\d*',v_tag.text)
                        temp_dict['title'] = tp[0]
                        temp_dict['comment'] = comment.strip()
                        temp_dict['timetable'] = timetable
                        temp_lst.append(temp_dict)
                        temp_dict = dict()
           
                df_source.extend(temp_lst)
                temp_lst.clear()
              
                
        
        
        time.sleep(1)
        
        df_source = [d for d in df_source if d['comment'] != '']
        
        comments_df = pd.DataFrame(df_source)
        try:
                comments_df.to_pickle('./data/comments.pkl')
        except:
                os.mkdir('./data')
                comments_df.to_picke('./data/comments.pkl')
            
      
        