from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time

class scrape:

    scraper = cloudscraper.create_scraper(delay=1,browser = 'chrome')
    
    def get_urls():
        urls = list()
        html_ll = scrape.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
        soup_ll = bs(html_ll.content,'html.parser')
        tags = soup_ll('a')
        urls = [tag.get('href',None) for tag in tags if len(tag.get('href',None)) > 2]
        return urls

    def scan_threads():
        df_lst = list()
        urls =scrape.get_urls()
        for url in urls:
                if len(url) < 2:
                        continue
                r = scrape.scraper.get(url)
                soup = bs(r.content,'html.parser')
                main_wrap = soup(class_ ='MAIN_WRAP')
                for tag in main_wrap:
                        temp_dict = {}
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
                temp_dict = {}
                time.sleep(1)
                
        threads_df = pd.DataFrame(df_lst)
        try:
                threads_df.to_pickle('./data/threads.pkl')
        except:
                os.mkdir('./data')
                threads_df.to_pickle('./data/threads.pkl')
                
    def get_title_list():  
        links = scrape.get_urls()
        titles_lst = list()
        temp_dict = dict()
        for link in links:
               if len(link) < 2:
                       continue
               r = scrape.scraper.get(link)
               soup = bs(r.content,'html.parser')
               main_wrap = soup(class_ ='MAIN_WRAP')
               for tag in main_wrap:
                       temp_dict = {}
                       temp_dict['title'] = soup.h1.text
                       temp_dict['link'] = link
                       titles_lst.append(temp_dict)
        temp_dict = {}
        time.sleep(1)
        
        titles_df = pd.DataFrame(titles_lst)
        try:
                titles_df.to_pickle('./data/titles.pkl')
        except:
                os.mkdir('./data')
                titles_df.to_pickle('./data/titles.pkl')
                
                
    def get_comments():
        df_source = list()
        with open('./data/titles.pkl') as df:
                df = df.loc[1:,['title','link']]
                dlst = list(zip(df['title'],df['link'])) 
        for tp in dlst:
                source = scrape.scraper.get(tp[1])
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
                        temp_dict = {}
                df_source.extend(temp_lst)
                temp_lst = []
                
                time.sleep(1)
      
       
        df_source = [d for d in df_source if d['comment'] != '']
       
        
        comments_df = pd.DataFrame(df_source)
        try:
                comments_df.to_pickle('./data/comments.pkl')
        except:
                os.mkdir('./data')
                comments_df.to_pickle('./data/comments.pkl')
       
     
            
scrape.get_comments()
      
        