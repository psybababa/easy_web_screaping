from bs4 import BeautifulSoup as bs
import cloudscraper
import json
import pandas as pd
import re
import requests
import time
import urllib.parse

class scrape:
        
    scraper = cloudscraper.create_scraper(delay=1,browser = 'chrome')
    params = {
            # 変化させたい検索用パラメータをdefaultsの様に書いてください。
    }
    
    def geturls():
        htmlll = scrape.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
        soupll = bs(htmlll.content,'html.parser')
        tags = soupll('a')
        urls = [tag.get('href',None) for tag in tags if len(tag.get('href',None)) > 2]
        return urls

    def searchurls(self):
        defaults = {
                'pnum':0,
                'rpp':100,
                'sword':0,
                'bbs':'livejupiter',
                'sorder':'updated',
                'sorder2':'ninzu'
        }
        
        urls = []
        searchurl = 'https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter'
        
        searchparams = {**defaults,**self.params}  # **でkeyとvalueをextractして、mergeする
        
        encodedq = urllib.parse.urlencode(searchparams)
        url = searchurl + encodedq
        
        htmlll = scrape.scraper.get(url) 
        soupll = bs(htmlll.content,'html.parser')
        tags = soupll('a')
        urls = [tag.get('href',None) for tag in tags if len(tag.get('href',None)) > 2]
        return urls

    def scanthreads():
        links =scrape.geturls()
        dfsource = {}
        
        for link in links:
                if len(link) < 2:
                        continue
                try:
                        r = scrape.scraper.get(link)
                        soup = bs(r.content,'html.parser')
                        title = soup.h1.text
                        comments = (soup.dl.dd.text).strip()
                        icchidatas = soup.dl.dt.text
                        nanashi = re.search('1 ：(...)',icchidatas)
                        date = re.search(r'\d*/\d*/\d*',icchidatas)
                        timetable= re.search(r'\d*:\d*:\d*',icchidatas)
                        id = re.search('ID:(....)',icchidatas)
                        
                        row = {'title':title, 'comments':comments, 'nanashi':nanashi, 'date':date,'timetable':timetable,'id':id}
                        dfsource[link] = row
                        
                        time.sleep(1)
                        
                except requests.exceptions.RequestException as e:
                        print(f'error happend while scraping{link}: {e}')
                        continue
               
        with open('./data/threads.json','wb') as f:
                json.dump(dfsource)
                
        threads_data = [{'link':key, **val} for key,val in dfsource.items()]
        threads_df = pd.json_normalize(threads_data)

        with open('./data/threads.pkl', 'wb') as f:
            threads_df.to_pickle(f)
      
                
    def gettitlelist():
        links = scrape.geturls()
        dfsource = []
        for link in links:
            if len(link) < 2:
                continue
            try:
                r = scrape.scraper.get(link)
                soup = bs(r.content, 'html.parser')
                title = soup.h1.text 
                row = {'title': title, 'link': link}
                
                dfsource.append(row)
                
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while accessing {link}: {e}")
                continue
    
        titlesdf = pd.DataFrame(dfsource)
    
        with open('./data/titles.pkl', 'wb') as f:
            titlesdf.to_pickle(f)
                
        
    def getcomments():
            titlesdf = pd.read_pickle('./data/titles.pkl').iloc[1:, ['title', 'link']]
            dfsource = [{'title': title, 'link': link} for title, link in zip(titlesdf['title'], titlesdf['link'])]
            for row in dfsource:
                source = scrape.scraper.get(row['link'])
                soup = bs(source.content, 'html.parser')
                valtags = soup.find_all(class_=re.compile('mesg hd'), attrs={'body', 'value'})
                
                row.update({'comments': [
                    {'comment': vtag.dd.text.strip(), 'timetable': re.findall(r'\d*:\d*:\d*', vtag.text)}
                    for vtag in valtags if not re.search('!AA|imgur|http', vtag.dd.text)
                ]})
                
                time.sleep(1)
                
                with open('./data/comments.json','wb') as f:
                        json.dump(dfsource)
        
            commentsdf = pd.json_normalize(dfsource, ['comments'], ['title', 'link']).dropna(subset=['comment'])
        
            with open('./data/comments.pkl', 'wb') as f:
                commentsdf.to_pickle(f)
        
 
            