from yeksatr.backend.helpers.utility import get_md5_hash, encode_to_utf8, pretty_date, mysql_str
from yeksatr.backend.helpers.setting import Setting
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
    
    def get_news(self,start=0,limit=50):
        query = (News.select(News.title,News.url.alias('link'),News.id,News.publish_date,
                fn.Concat(Setting.rss_icon_path,Source.icon).alias('icon'),Source.title.alias('icon_title'),
                fn.timestampdiff(SQL('SECOND'),News.publish_date,fn.utc_timestamp() ).alias('seconds')).
                join(Feed).join(Source).naive().order_by(News.publish_date.desc()).limit(limit).execute())
        for item in query:
            item.publish_date =  pretty_date(item.seconds)
        return query
        
    def get_all(self):
        pass
    
    def get_unextracted_news(self,count):
        query = (News.select(News.id,News.url,SourceTag.tag_class,SourceTag.tag_name,SourceTag.tag.alias('tag_id'))
                .join(Feed).join(Source).join(SourceTag).naive().where(News.extracted==0).limit(count).execute() )
        return query
    
    def add_content(self,news_id,html,text):
        NewsContent.create(fk_news=news_id,html_content=html,text_content=text)
        News.update(extracted=1).where(News.id==news_id).execute()
        
