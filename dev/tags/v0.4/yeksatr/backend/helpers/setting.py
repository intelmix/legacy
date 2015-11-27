from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase
from pyramid.request import Request

from yeksatr.backend.helpers.logutil import LogUtil
class Setting(object):
    
    temp_var = "ya"
    #path
    rss_icon_path = "/static/images/favicons/"
    main_log_path = 'log/error.log'
    session_dir =  'log/session'
    cookie_path = '/'
    
    include_path = ["src","src/libs","src/libs/html5lib"]
    
    
    
    #public config
    log_enable = True
    debuging = True
    persian_timezone_seconds = 4.5*60*60
    session_timeout = 1*60*60 #1hour
    home_page_news = 50
    crawl_interval = 5*60
    
    #shared objects    
    sid = None
    error_log = LogUtil(main_log_path,log_enable,debuging)
    
    db = {'host':'127.0.0.1','db_name':'beta_yeksatr','user':'beta_user','pass':'ykstr_beta_user%$#@'}    
    
    
   
    database = MySQLDatabase(None)
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
def InitSetting(mode='beta'):
    if mode == 'beta':
        pass
    else:
        Setting.db['host']  = '127.0.0.1'
        Setting.db['db_name'] = 'live_yeksatr'
        Setting.db['user'] = 'live_user'
        Setting.db['pass'] = 'ykstr_thisislive_#$%_'
    
    
    
def InitDB():    
    #Setting.database = MySQLDatabase(None)
    try:
        try:
            Setting.database.close()
        except Exception as e:
            Setting.error_log.LogException(e,' error in closing previus connection (Setting.InitDB): ')
            pass
        Setting.database.init(Setting.db['db_name'],  host=Setting.db['host'],passwd = Setting.db['pass'], user = Setting.db['user'])
    except Exception as ex:
        Setting.error_log.LogException(ex,' error in connecting to database: ')
        