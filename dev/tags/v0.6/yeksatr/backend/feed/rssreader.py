# coding: utf-8
import feedparser
import time
import os,sys,traceback
import urllib
from operator import attrgetter 
import datetime

from yeksatr.backend.helpers import jdate
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers.utility import EncodeToUtf8
from yeksatr.backend.helpers import jdatetime
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.orm.model import *


def myDateHandler(aDateString):
    patterns = ["%d %B %Y %H:%M:%S",
                "%Y/%m/%d - %H:%M:%S"]
    for pt in patterns:
        try:
            tt = time.strptime(aDateString, pt)
            return tt
        except Exception as ex:
            Setting.log.LogException( ex,'date convertion ' )
            pass    
    return None
#feedparser.registerDateHandler(myDateHandler)



class RssReader(object):
    def __init__(self):
        pass
    
    def IsCrawlTime(self):
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
    def SetCrawlLog(self,news_count=0):
        CrawlLog.create(news_count=news_count)
        
        
    def Read(self):
        if self.IsCrawlTime() == False:
            return 0
       
        urls = Feed.select().execute()
        
        result = []
        entries = []
        news_count = 0
        nw = NewsWorker()
        for url in urls:            
            try:
                d = feedparser.parse(url.url)                
                rss_title = EncodeToUtf8(d['feed']['title'])                
                for item in d.entries:
                    gmt_date,persian_date = self.ComputeDates(item.published, item.published_parsed)
                    date,time = self.GetJalaliDateTime(persian_date)
                    if nw.AddNews(item.title, item.link, url.id, gmt_date) :
                        news_count += 1                          
            except Exception as ex:    
                Setting.log.LogException(ex,'rss reading main loop: ')           
                
                
                
        self.SetCrawlLog(news_count)
       
        return news_count
    
    def ComputeDates(self,date_str,gmt_date):
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
                    Setting.log.LogException(ex, 'date convertion '  )
                    pass    
        else:           
            gmt_date = datetime.datetime(gmt_date.tm_year,gmt_date.tm_mon,gmt_date.tm_mday,gmt_date.tm_hour,gmt_date.tm_min,gmt_date.tm_sec)      
            
        tmp_date = gmt_date + datetime.timedelta(0,Setting.persian_timezone_seconds)         
        persian_date=jdatetime.datetime.fromgregorian(datetime=tmp_date)
        return gmt_date,persian_date
    
    
    
    def GetJalaliDateTime(self,tt,return_str=True):        
        y,m,d,h,mi,s = tt.year,tt.month,tt.day,tt.hour,tt.minute,tt.second
        
        
        if return_str:
            mon = jdate.GetPersianMonth(m)
            
            return  u'%d %s %d ' % (d,mon,y) , '%02d:%02d:%02d' % (h,mi,s) 
            #return  "%d/%02d/%02d %02d:%02d:%02d" % (y,m,d,h,mi,s)
        else:
            return time.struct_time(y,m,d,h,mi,s)
    
   
        
     
    
          
    