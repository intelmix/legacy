import configparser,sys

from yeksatr.backend.helpers.setting import init_setting, init_db
from yeksatr.backend.helpers.setting import Setting

from feed.rssreader import RssReader
from feed.newsagent import NewsAgent

if __name__ == '__main__':
    path = "../development.ini";
    config = configparser.ConfigParser()
    config.read(path)
    init_setting(config)
    init_db()
 
    for i in range(len(sys.argv)):
        param = sys.argv[i]
        if param == '-update' :
            rr = RssReader()
            rr.read()
            pass
        elif param == '-extract':
            na = NewsAgent()    
            na.extract_news(30)
            pass
    

    print ("jobs done")
    pass