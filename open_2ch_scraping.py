from bs4 import BeautifulSoup as bs
import cloudscraper
import pandas as pd
import re
import time

class scrape_onj:

    def __init__(self):
            self.scraper = cloudscraper.create_scraper(delay=1, browser="chrome") #cloudflareサーバーの1020エラーによるブロックを防ぐためrequestsではなくcloudscraperを用いる。尚、おーぷん2chではプロクシは使用できない。
        
    def get_links():
    #スクレイピング作業をまずはおんJのスレッド一覧で行い、リンクを手に入れる。
        links = list()
        html_ll = scrape_onj.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
        soup_ll = bs(html_ll.content,'html.parser')
        tags = soup_ll('a')
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
        thereads_df.to_pickle('C:\Users\Clean\Documents\workspace\easy_scraping\data\threads.pkl')
        
    def parse_res(self):  
        #指定したスレッド内をスクレイピングして、レスだけを抽出していく。こっちは一つのスレッドに対して行う
        while True:
                add = input('レスを集めたいスレのURLを入力してくれや*終了したい時はq入力してな:')
                if len(add) < 1:
                        print('URL入力してくれや；；')
                        continue
                if add == 'q' or add == 'Q':
                        print('ご利用ありがとござます🥺')
                        quit()
                res = self.scraper.get()
        
        
#scrape_onj.parse_thread()