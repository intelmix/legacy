# coding: utf-8
import feedparser
import time
import os,sys,traceback
import urllib
from operator import attrgetter 
import datetime

from yeksatr.backend.helpers import jdate
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers.utility import encode_to_utf8
from yeksatr.backend.helpers import jdatetime
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.orm.model import *

def my_date_handler(aDateString):
    patterns = ["%d %B %Y %H:%M:%S",
                "%Y/%m/%d - %H:%M:%S"]
    for pt in patterns:
        try:
            tt = time.strptime(aDateString, pt)
            return tt
        except Exception as ex:
            Setting.log.log_exception( ex,'date convertion ' )
            pass    
    return None
#feedparser.registerDateHandler(my_date_handler)

class RssReader(object):
    def __init__(self):
        pass
    
    def is_crawl_time(self):
        if CrawlLog.select().count() == 0:
            return True
        query = (CrawlLog.select(
                fn.timestampdiff(SQL('SECOND'),CrawlLog.crawl_date,fn.now() ).alias('seconds') )
                .order_by(CrawlLog.crawl_date.desc()).limit(1)   ).get()
                 
        if query.seconds >= Setting.crawl_interval:
        
            return True
        else:
            return False
        
        return True
    
    def set_crawl_log(self,news_count=0):
        CrawlLog.create(news_count=news_count)
        
    def read(self):
        if self.is_crawl_time() == False:
            return 0
       
        urls = Feed.select().execute()    
        
        result = []
        entries = []
        news_count = 0
        nw = NewsWorker()
        
        for url in urls: 
                       
            try:
                
                try:
                    Setting.log.info("start crawing for "+url.url)
                except:
                    pass
                d = feedparser.parse(url.url)        
                   
                rss_title = encode_to_utf8(d['feed']['title'])                
                for item in d.entries:
                    if hasattr(item,'published'):                        
                        gmt_date,persian_date = self.compute_dates(item.published, item.published_parsed)
                    else:
                        gmt_date = datetime.datetime.now()
                        gmt_date -= datetime.timedelta(0,Setting.persian_timezone_seconds) 
                    #date,time = self.get_jalali_datetime(persian_date)
                    if nw.add_news(item.title, item.link, url.id, gmt_date) :
                        news_count += 1                          
            except Exception as ex:    
                Setting.log.log_exception(ex,'rss reading main loop: ')           
                
                
                
        self.set_crawl_log(news_count)
       
        return news_count
    
    def compute_dates(self,date_str,gmt_date):
        persian_date=None
        if gmt_date == None :               
            patterns = [{'format':"%Y/%m/%d - %H:%M:%S",'diff':Setting.persian_timezone_seconds}]
            for pt in patterns:
                try:
                    tt = jdatetime.datetime.strptime(date_str,pt['format'])
                    
                    persian_date= tt
                    gmt_date = persian_date.togregorian()
                    
                    gmt_date -= datetime.timedelta(0,pt['diff']) 
                    
                    break
                except Exception as ex:
                    Setting.log.log_exception(ex, 'date convertion '  )
                    pass    
        else:           
            gmt_date = datetime.datetime(gmt_date.tm_year,gmt_date.tm_mon,gmt_date.tm_mday,gmt_date.tm_hour,gmt_date.tm_min,gmt_date.tm_sec)      
            
        tmp_date = gmt_date + datetime.timedelta(0,Setting.persian_timezone_seconds)         
        persian_date=jdatetime.datetime.fromgregorian(datetime=tmp_date)
        return gmt_date,persian_date    
    
    def get_jalali_datetime(self,tt,return_str=True):        
        y,m,d,h,mi,s = tt.year,tt.month,tt.day,tt.hour,tt.minute,tt.second        
        
        if return_str:
            mon = jdate.GetPersianMonth(m)
            
            return  u'%d %s %d ' % (d,mon,y) , '%02d:%02d:%02d' % (h,mi,s) 
            #return  "%d/%02d/%02d %02d:%02d:%02d" % (y,m,d,h,mi,s)
        else:
            return time.struct_time(y,m,d,h,mi,s)
