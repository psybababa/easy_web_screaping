from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time

class scrape:

    scraper = cloudscraper.create_scraper(delay=1,browser = 'chrome')
    
    def geturls():
        urls = list()
        htmlll = scrape.scraper.get('https://hayabusa.open2ch.net/headline.cgi?bbs=livejupiter') 
        soupll = bs(htmlll.content,'html.parser')
        tags = soupll('a')
        urls = [tag.get('href',None) for tag in tags if len(tag.get('href',None)) > 2]
        return urls

    def scanthreads():
        dflst = list()
        tempdict = dict()
        urls =scrape.geturls()
        
        for url in urls:
                if len(url) < 2:
                        continue
                
                try:
                        r = scrape.scraper.get(url)
                        soup = bs(r.content,'html.parser')
                        mainwrap = soup(class_ ='MAIN_WRAP')
                        for tag in mainwrap:
                                tempdict['title'] = soup.h1.text
                                tempdict['comments'] = (soup.dl.dd.text).strip()
                                icchidatas = soup.dl.dt.text
                                nanashi = re.findall('1 ：(...)',icchidatas)
                                date = re.findall(r'\d*/\d*/\d*',icchidatas)
                                timetable= re.findall(r'\d*:\d*:\d*',icchidatas)
                                id = re.findall('ID:(....)',icchidatas)
                                tempdict['nanashi'] = nanashi[0]
                                tempdict['date'] = date[0]
                                tempdict['timetable'] = timetable[0]
                                tempdict['id'] = id[0]
                                dflst.append(tempdict)
                                tempdict = {}
                except:
                        print(f'error happend while scraping{url}')
                        continue
               
                time.sleep(1)
                
        threadsdf = pd.DataFrame(dflst)
        
        if not os.path.exists('./data'):
                os.mkdir('./data')
                
        threadsdf.to_pickle('./data/threads.pkl')
      
                
    def gettitlelist():  
        links = scrape.geturls()
        titleslst = list()
        tempdict = dict()
        
        for link in links:
               if len(link) < 2:
                       continue
               try:
                       r = scrape.scraper.get(link)
                       soup = bs(r.content,'html.parser')
                       mainwrap = soup(class_ ='MAIN_WRAP')
                       for tag in mainwrap:
                               tempdict['title'] = soup.h1.text
                               tempdict['link'] = link
                               titleslst.append(tempdict)
                               tempdict = {}
               except:
                       print(f'Error happend while scraping {link}')
                       continue
               
               time.sleep(1)
        
        titlesdf = pd.DataFrame(titleslst)
        
        if not os.path.exists('./data'):
                os.mkdir('./data')
        
        titlesdf.to_pickle('./data/titles.pkl')
                
                
    def getcomments():
        dfsource = list()
        titlesdf = pd.read_pickle('./data/titles.pkl')
        titlesdf = titlesdf.loc[1:,['title','link']]
        dlst = list(zip(titlesdf['title'],titlesdf['link'])) 
        for tp in dlst:
                source = scrape.scraper.get(tp[1])
                soup = bs(source.content,'html.parser')
                valtags = soup.find_all(class_ = re.compile('mesg hd'),attrs={'body','value'})
                templst = list()
                for vtag in valtags:
                        tempdict = dict()
                        comment = vtag.dd.text
                        if re.search('!AA|imgur|http',comment):
                                continue
                        timetable = re.findall(r'\d*:\d*:\d*',vtag.text)
                        tempdict['title'] = tp[0]
                        tempdict['comment'] = comment.strip()
                        tempdict['timetable'] = timetable
                        templst.append(tempdict)
                        tempdict = {}
                dfsource.extend(templst)
                templst = []
                
                time.sleep(1)
      
       
        dfsource = [d for d in dfsource if d['comment'] != None]
       
        
        commentsdf = pd.DataFrame(dfsource)
        
        if not os.path.exists('./data'):
                os.mkdir('./data')
        commentsdf.to_pickle('./data/comments.pkl')
        
        
