from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase
from pyramid.request import Request
from yeksatr.backend.helpers.logutil import LogUtil

class Setting(object):
    #path
    rss_icon_path = ""
    main_log_path = ''
    
    #public config
    log_enable = True
    debuging = True
    persian_timezone_seconds = 0   
    home_page_news = 0
    crawl_interval = 0
    log_level=0
    
    #shared objects    
    sid = None    
    log = LogUtil(enable=False)    
    db = {}       
    database = MySQLDatabase(None)
    
    def __init__(self, params):
        pass

    def init_setting(app_info):
        mode = app_info.get('app:main','mode')
        Setting.db['host']  = app_info.get('yeksatr:config','db_host')
        Setting.db['db_name'] = app_info.get('yeksatr:config','db_name')
        Setting.db['user'] = app_info.get('yeksatr:config','db_user')
        Setting.db['pass'] = app_info.get('yeksatr:config','db_pass')
        Setting.mode = mode

        Setting.rss_icon_path = app_info.get('yeksatr:config','rss_icon_path')
        Setting.main_log_path = app_info.get('yeksatr:config','main_log_path')   

        #public config
        Setting.log_enable = app_info.getboolean('yeksatr:config','log_enable')
        Setting.debuging = app_info.getboolean('yeksatr:config','debuging')
        Setting.persian_timezone_seconds =app_info.getint('yeksatr:config','persian_timezone_seconds')  
        Setting.home_page_news = app_info.getint('yeksatr:config','home_page_news')
        Setting.crawl_interval = app_info.getint('yeksatr:config','crawl_interval')
        Setting.log_level = app_info.getint('yeksatr:config','log_level')

        Setting.log = LogUtil(Setting.main_log_path,Setting.log_level,Setting.log_enable)

    def init_db():    
        try:
            try:
                Setting.database.close()
            except Exception as e:
                Setting.log.log_exception(e,' error in closing previus connection (Setting.init_db): ')
                pass
                Setting.database.init(Setting.db['db_name'],  host=Setting.db['host'],passwd = Setting.db['pass'], user = Setting.db['user'])
            except Exception as ex:
                Setting.log.log_exception(ex,' error in connecting to database: ')

    def test(request,a):
        print(request,a)
