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
 
