# coding: utf-8
# -*- coding: utf-8 -*-
from yeksatr.backend.helpers.setting import Setting

def encode_to_utf8(str):
    #return str
    try:
        #tmp = str.encode('utf-8','ignore')
        tmp = str.encode(encoding="utf-8", errors="strict")
        return tmp.decode()
    except:        
        return str 

def is_null(val):
    if val == None:
        return True
    if val == '' or val == "":
        return True
    return False

def get_md5_hash(strr):
    import hashlib
    return hashlib.md5(strr).hexdigest()
    

def pretty_date(seconds):
    a_min = 60
    a_hour = 60*a_min
    a_day = 24 * a_hour
    a_week = a_day*7
    a_month = a_day * 30
    a_year = a_month * 12
    if seconds <0 :
        seconds = 0
    years = int(seconds / a_year)
    months = int((seconds %a_year)/a_month)
    weeks = int((seconds % a_month) / a_week)
    days = int((seconds % a_week) / a_day)
    hours = int((seconds %a_day)/a_hour)
    mins = int((seconds%a_hour)/a_min)
    
    #print(years,months,weeks,days,hours,mins)
    
    if years == 0:
        if months == 0:
            if weeks == 0:
                if days == 0:
                    if hours == 0:
                        if mins<3 :
                            return u"همین الان"                        
                        else :
                            return u"%d دقیقه  پیش"%(mins)                        
                    else:
                        if min == 0:
                            return u"%d ساعت پیش"%(hours)
                        else:
                            return u"%d ساعت و %d دقیقه پیش"%(hours,mins)                    
                else:                    
                        return u"%d روز پیش"%(days)
                    
            else:
                if days == 0:
                    return u"%d هفته پیش"%(weeks)
                else:
                    return u"%d هفته و %d روز پیش"%(weeks,days)                
            
        elif months == 1:
            if weeks == 0:
                return u"%d ماه پیش"%(months)
            else:
                return u"%d ماه و %d هفته پیش"%(months,weeks)
        else:
            return u"%d ماه پیش"%(months)
        
    elif years == 1:
        if months == 0:
            return u"%d سال پیش"%(years)
        else:
            return u"%d سال و %d ماه پیش"%(years,months)  
        
    else:
        return u"%d سال پیش"%(years)
        
    
    return '--:--:--'

def pretty_date_old(seconds):
    a_min = 60
    a_hour = 60*a_min
    a_day = 24 * a_hour
    a_week = a_day*7
    a_month = a_day * 30
    a_year = a_month * 12
    
    years = int(seconds / a_year)
    months = int((seconds %a_year)/a_month)
    weeks = int((seconds % a_month) / a_week)
    days = int((seconds % a_month) / a_day)
    hours = int((seconds %a_day)/a_hour)
    mins = int((seconds%a_hour)/a_min)
    
    #print(years,months,weeks,days,hours,mins)
    
    if years == 0:
        if months == 0:
            if weeks == 0:
                if days == 0:
                    if hours == 0:
                        if mins<5 :
                            return u"همین الان"
                        elif mins <20:
                            return u"چند دقیقه پیش"
                        elif mins < 45 :
                            return u"تقریبا نیم ساعت پیش"
                        else :
                            return u"تقریبا یک ساعت پیش"
                        
                    else:
                        return u"%d ساعت و %d دقیقه پیش"%(hours,mins)                    
                else:
                    if hours == 0 :
                        return u"%d روز پیش"%(days)
                    else :
                        return u"%d روز و %d ساعت پیش" %(days,hours)
            else:
                return u"%d هفته و %d روز پیش"%(weeks,days)
                
            
        elif months < 2:
            if weeks == 0:
                return u"%d ماه پیش"%(months)
            else:
                return u"%d ماه و %d هفته پیش"%(months,weeks)
        else:
            return u"%d ماه پیش"%(months)
        
    elif years == 1:
        if months == 0:
            return u"%d سال پیش"%(years)
        else:
            return u"%d سال و %d ماه پیش"%(years,months)  
        
    else:
        return u"%d سال پیش"%(years)
        
    
    return '--:--:--'


def fetch_url(url):
    import urllib.request as urllib2
    
    if url.startswith("http") == True :
        url = url.replace("http://","")
        
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.20) Gecko/20081217 Firefox/2.0.0.20"
    ,"Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
    ,"Accept-Charset" : "utf-8"
    }
    try:                
        #url  = urllib2.quote(url)
        url = "http://" + url            
        req = urllib2.Request(url, None, headers)                                
        page =  urllib2.urlopen(req,None)            
        return page.read()
    except Exception as ex:
        
        print (ex.__str__())
       
        
    return "problem"

def get_data(orig_url):
    import urllib.request as urllib2
    from urllib.parse   import quote
    #print(url)
    #url  = urllib2.quote(url)
    if orig_url.startswith("http") == True :
        orig_url = orig_url.replace("http://","")
        
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.20) Gecko/20081217 Firefox/2.0.0.20"
    ,"Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
    ,"Accept-Charset" : "utf-8"
    }
    try:
              
        url  = quote(orig_url)
        url = "http://" + url    
        #print(url)        
        req = urllib2.Request(url, None, headers)                                
        page =  urllib2.urlopen(req,None)            
        return page.read()
    except Exception as ex:     
        Setting.log.log_exception( ex,'fetching url with quoting : '  )
        #print( ex.__str__()+"  ")
       
    try:              
        #url  = quote(orig_url)
        url = "http://" + orig_url    
        #print(url)        
        req = urllib2.Request(url, None, headers)                                
        page =  urllib2.urlopen(req,None)            
        return page.read()
    except Exception as ex:     
        Setting.log.log_exception( ex,'fetching url without quoting : ' )
        #print( ex.__str__()+"  ")
       
        
    return "problem"



def mysql_str(star):
    import pymysql
    return  pymysql.escape_string(star)
