# coding: utf-8
# -*- coding: utf-8 -*-
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers.utility import FetchUrl, EncodeToUtf8, MysqlStr,GetData

 
class NewsAgent(object):

    def __init__(self):        
        pass
    
    def ExtractNews(self,count=10):               
        n = NewsWorker()
        items = n.GetUnextractedNews(count)
        for item in items:
            try:
                url =  item.url
                print(url)
                id =  item.id
                tag_name = item.tag_name
                tag_class = item.tag_class
                tag_id = item.tag_id
               
                page = GetData(url)              
                text,html = self.Extract(page.decode('utf-8'),tag_name,tag_class,tag_id)                
                
                n.AddContent(id, MysqlStr(html), MysqlStr(text))
            except Exception as ex:
                Setting.error_log.LogException(ex)
            return

        
        
    def Extract(self,page,tag_name,tag_class,tag_id):
        from bs4 import BeautifulSoup
        from bs4 import SoupStrainer
        import html5lib

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