from yeksatr.backend.helpers.utility import get_md5_hash, encode_to_utf8, pretty_date, mysql_str
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.helpers import jdatetime
import datetime
from .model  import *

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
    
    def get_news(self,filter,start=0,limit=50):
        query = (News.select(News.title,News.url.alias('link'),News.id,News.publish_date,News.publish_date.alias("datey"),
                fn.Concat(Setting.rss_icon_path,Source.icon).alias('icon'),Source.title.alias('icon_title'),
                fn.timestampdiff(SQL('SECOND'),News.publish_date,fn.utc_timestamp() ).alias('seconds')).
                where(fn.fix_arabic_char(News.title) ** fn.fix_arabic_char('%'+filter+'%')).
                #where( SQL('match(t1.title) against("'+filter+'" IN BOOLEAN MODE )') ).
                join(Feed).join(Source).naive().order_by(News.publish_date.desc()).limit(limit).execute()) 
         
        for item in query: 
            item.datey += datetime.timedelta(0,Setting.persian_timezone_seconds)
            tt = jdatetime.datetime.fromgregorian(datetime=item.datey)
            
            item.datey = tt.strftime("%d %B %Y ساعت  %H:%M")
            
            item.publish_date =  pretty_date(item.seconds)
        return query
            
    def get_unextracted_news(self,count):
        query = (News.select(News.id,News.url,SourceTag.tag_class,SourceTag.tag_name,SourceTag.tag.alias('tag_id'))
                .join(Feed).join(Source).join(SourceTag).naive().where(News.extracted==0).limit(count).execute() )
        return query
    
    def add_content(self,news_id,html,text):
        NewsContent.create(fk_news=news_id,html_content=html,text_content=text)
        News.update(extracted=1).where(News.id==news_id).execute()
        
