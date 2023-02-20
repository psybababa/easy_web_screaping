from bs4 import BeautifulSoup
import cloudscraper
import re

scraper = cloudscraper.create_scraper(delay=1, browser="chrome")

temp_lst = list()

url = 'https://hayabusa.open2ch.net/test/read.cgi/livejupiter/1676840860/l10'
source = scraper.get(url)

soup = BeautifulSoup(source.content, 'html.parser')
val_tags = soup.find_all(class_ = re.compile('mesg hd'), attrs={'body', 'value'})

for v_tag in val_tags:
    temp_dict = dict()
    timetable = re.findall(r'\d*:\d*:\d*',v_tag.text)
    comment = v_tag.dd.text
    temp_dict['comment'] = comment.strip()
    temp_dict['timetable'] = timetable                       
    temp_lst.append(temp_dict)
print(temp_lst)