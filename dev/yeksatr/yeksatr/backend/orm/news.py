# coding: utf-8
# -*- coding: utf-8 -*-
from yeksatr.backend.helpers.utility import get_md5_hash, encode_to_utf8, pretty_date, mysql_str
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers import jdatetime
import datetime
from .model  import *
from peewee import JOIN_RIGHT_OUTER
import array
from _ast import List
from yeksatr.backend.orm.model import Bulletin

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
    
    def get_news(self,filter,source,days,starred,user_id,start=0,limit=50):
        query = (UserNews.select(News.title,News.url.alias('link'),News.id,News.publish_date,News.publish_date.alias("persian_date"),
                fn.Concat(Setting.rss_icon_path,Source.icon).alias('icon'),Source.title.alias('icon_title'),
                fn.timestampdiff(SQL('SECOND'),News.publish_date,fn.utc_timestamp() ).alias('seconds'),UserNews.is_starred).
                 #where(user_id ==None | UserNews.fk_user == user_id ).
                          
                join(News,JOIN_RIGHT_OUTER).join(Feed).join(Source).
                where( (fn.fix_arabic_char(News.title) ** fn.fix_arabic_char('%'+filter+'%') ) & 
                      (  (SQL('fk_user_id is null')) | (UserNews.fk_user == user_id ) ) &
                      (True if source == None or user_id==None  else  Source.id==source) &
                      (True if starred == None or starred==False else UserNews.is_starred==starred) &
                      (True if days == None or user_id==None else fn.timestampdiff(SQL('DAY'),News.publish_date,fn.utc_timestamp() )<= days ) ).
                naive(). order_by(News.publish_date.desc(), News.id.desc()).limit(limit).      
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
        
    def get_all_sources(self):
        query = Source.select(Source.id,Source.title,fn.Concat(Setting.rss_icon_path,Source.icon).alias('icon')).execute()
        #return query
        res = []
       
        for item in query:
            
            res.append({'id':item.id,'title':item.title,'icon':item.icon})
                
        return res
    def add_bulletin(self,user_id,query_text,scan_period,source,starred,bulletin_id):
        b = Bulletin()
        if   bulletin_id >= 0 :
            b = Bulletin.get(Bulletin.id == bulletin_id)
        
        b.fk_user = user_id
        b.save()
        
        bf = BulletinFilter()
        if bulletin_id >= 0 :
            tmp = BulletinFilter.select().where(BulletinFilter.fk_bulletin == b.id )
            for tt in tmp :
                bf = tt
                break
        
        bf.fk_bulletin = b.id
        bf.fk_source = source if source >=0 else None
        bf.query_text = query_text        
        bf.scan_period = scan_period if scan_period >=0 else None  
        bf.starred = 0 if starred == 'false' else 1
        
        bf.save()
        
    def get_user_bulletin(self, user_id):
        
        query = (Bulletin.select(Bulletin.id, BulletinFilter.query_text, Source.title.alias('source'),
                                 BulletinFilter.scan_period, BulletinFilter.starred, Source.id.alias('source_id'))
                .join(BulletinFilter).join(Source,JOIN_LEFT_OUTER).naive().where(Bulletin.fk_user == user_id))
        ll = []
        
        if query.count() > 0 :
            query = query.execute()
            for index, ft  in enumerate(query):
                ll.append({'index':index + 1, 'query_text':ft.query_text, 'source':ft.source, 'id':ft.id, 'source_id':ft.source_id,
                           'scan_period':ft.scan_period, 'starred':ft.starred})
        return ll
        
        '''
        query = (Bulletin.select(Bulletin.id,Bulletin.title,Bulletin.recipient_email,fn.count(BulletinFilter.id).alias('cnt'))
                 .join(BulletinFilter,JOIN_LEFT_OUTER).group_by(Bulletin.id,Bulletin.title,Bulletin.recipient_email).where(Bulletin.fk_user == user_id ).execute())
        ll = []
        for index,bt  in enumerate( query):
            ll.append({'index':index+1,'email':bt.recipient_email,'title':bt.title,'cnt':bt.cnt,'id':bt.id})
        return ll'''
    
    def add_bulletin_filter(self,bulletin_id,source_id,query_text):
        f = BulletinFilter()
        f.fk_bulletin = bulletin_id
        f.fk_source = source_id if source_id >=0 else None
        f.query_text = query_text
        f.save()
        
    def get_bulletin_filter(self,bulletin_id,user_id):
        query = (Bulletin.select(Bulletin.id,fn.isnull(BulletinFilter.query_text,"").alias('query_text'),
                                 fn.isnull(Source.title,SQL("'همه منابع'")).alias('source') )
                 .join(BulletinFilter).join(Source).naive().where(Bulletin.id==bulletin_id , Bulletin.fk_user== user_id ).execute())
        
        ll = []
        for index,ft  in enumerate( query):
            ll.append({'index':index+1,'query_text':ft.query_text if ft.query_text != None else '' ,
                       'source':ft.source ,'id':ft.id,'source_id':ft.source_id})
        return ll
    
    def remove_bulletin_filter(self,filter_id,user_id):
        query = Bulletin.select().join(BulletinFilter).where(BulletinFilter.id == filter_id , Bulletin.fk_user == user_id)
        if query.count() > 0 :
            query = (BulletinFilter.delete().where(BulletinFilter.id== filter_id).execute())
            return True
        return False
            
    def remove_bulletin(self,bulletin_id,user_id):
        query = Bulletin.select().where(Bulletin.id == bulletin_id , Bulletin.fk_user == user_id)
        if query.count() > 0 : 
            BulletinFilter.delete().where(BulletinFilter.fk_bulletin == bulletin_id).execute()
            query = (Bulletin.delete().where(Bulletin.id== bulletin_id).execute())
            return True
        return False    
            
    def add_source(self,title,url,icon):
        s = Source()
        s.title = title
        s.icon = icon
        s.url = url
        s.save()

    def get_source_feed(self,source):
        query = Feed.select().where(Feed.fk_source == source ).execute()
        ll = []
        for index,f  in enumerate( query):
            ll.append({'index':index+1,'title':f.title , 'url':f.url})
        return ll
    
    def add_feed(self,source,title,url):
        f = Feed()
        f.fk_source = source
        f.title = title
        f.url = url
        f.save()
        