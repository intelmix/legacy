# coding: utf-8
# -*- coding: utf-8 -*-
from yeksatr.backend.helpers.utility import get_md5_hash, encode_to_utf8, pretty_date, mysql_str
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers import jdatetime
import datetime
from .model  import *
from peewee import JOIN_RIGHT_OUTER

class NewsWorker(object):   
    id = 0
    title = ''
    url = ''
    fk_feed_id = ''
    publish_date = None
    fetch_date = None
    url_hash = ''    
    
    def __init__(self):
        pass    
    
    def add_news(self, title, url, feed_id, publish_date):
        try:                   
            url_hash = get_md5_hash(url.encode('utf-8'))  
            cnt = News.select().where(News.url_hash==url_hash).count()          
            
            if cnt == 0:
                nw = News(title = title,url = url,url_hash = url_hash,fk_feed = feed_id,publish_date = publish_date);                
                nw.save()                                                    
                return True
            
            return False
        except Exception as ex:
            Setting.log.log_exception( ex,'news inserting to db : ' )
        pass
    
    def get_news(self,filter,user_id,start=0,limit=50):
        query = (UserNews.select(News.title,News.url.alias('link'),News.id,News.publish_date,News.publish_date.alias("persian_date"),
                fn.Concat(Setting.rss_icon_path,Source.icon).alias('icon'),Source.title.alias('icon_title'),
                fn.timestampdiff(SQL('SECOND'),News.publish_date,fn.utc_timestamp() ).alias('seconds'),UserNews.is_starred).
                 #where(user_id ==None | UserNews.fk_user == user_id ).
                          
                join(News,JOIN_RIGHT_OUTER).join(Feed).join(Source).
                where( (fn.fix_arabic_char(News.title) ** fn.fix_arabic_char('%'+filter+'%') ) & 
                      (  (SQL('fk_user_id is null')) | (UserNews.fk_user == user_id ) ) ).
                naive(). order_by(News.publish_date.desc()).limit(limit).      
                execute())
                
         #where( SQL('match(t1.title) against("'+filter+'" IN BOOLEAN MODE )') ).
         #, user_id != None and UserNews.fk_user==user_id
         
        for item in query: 
            item.persian_date += datetime.timedelta(0,Setting.persian_timezone_seconds)
            tt = jdatetime.datetime.fromgregorian(datetime=item.persian_date)
            
            item.persian_date = tt.strftime(u"%d %B %Y ساعت  %H:%M")
            
            item.publish_date =  pretty_date(item.seconds)
        return query
            
    def get_unextracted_news(self,count):
        query = (News.select(News.id,News.url,SourceTag.tag_class,SourceTag.tag_name,SourceTag.tag.alias('tag_id'))
                .join(Feed).join(Source).join(SourceTag).naive().where(News.extracted==0).limit(count).execute() )
        return query
    
    def add_content(self,news_id,html,text):
        NewsContent.create(fk_news=news_id,html_content=html,text_content=text)
        News.update(extracted=1).where(News.id==news_id).execute()
        
    def add_user_news(self,user_id,news_id):
        query =  UserNews.select().where(UserNews.fk_user==user_id,UserNews.fk_news==news_id)
        cnt = query.count()
        result = 'starred'
        if cnt == 0:
            obj = UserNews(fk_user=user_id,fk_news=news_id,title='',is_flagged=0,is_starred=1,news_content='',tags='')
            obj.save()
        else:
            news = query.execute()
            for item in news:
                if item.is_starred == 1:
                    item.is_starred = 0      
                    result = 'unstarred'              
                else:
                    item.is_starred = 1
                item.save()
            #UserNews.update(is_starred=1+ UserNews.is_starred).where(UserNews.fk_user==user_id,UserNews.fk_news==news_id).execute()
            
        return result
        
