# coding: utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import html5lib


from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers.utility import fetch_url, encode_to_utf8, mysql_str,get_data

 
class NewsAgent(object):

    def __init__(self):        
        pass
    
    def extract_news(self,count=10):            
        n = NewsWorker()
        items = n.get_unextracted_news(count)        
        for item in items:
            try:
                url =  item.url
                #print(url)
                id =  item.id
                tag_name = item.tag_name
                tag_class = item.tag_class
                tag_id = item.tag_id
               
                page = get_data(url)              
                text,html = self.extract(page.decode('utf-8'),tag_name,tag_class,tag_id)                
                
                n.add_content(id, mysql_str(html), mysql_str(text))
            except Exception as ex:
                Setting.log.log_exception(ex)
        
        
    def extract(self,page,tag_name,tag_class,tag_id):        
        soup = BeautifulSoup(page)
        #soup = BeautifulSoup(page,parseOnlyThese=SoupStrainer('div'))
        
        attr = dict()
        if tag_class != '':
            attr['class'] = tag_class
        if tag_id != '':
            attr['id'] = tag_id        
        
        res = soup.find(tag_name, attr)
        if res == None:
            return ' ',' '
        
        return res.get_text(),str(res)