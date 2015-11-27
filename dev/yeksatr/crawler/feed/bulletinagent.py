# -*- coding: utf8 -*-
# encoding=utf8 
'''
Created on Feb 11, 2015

@author: hossein
'''
from yeksatr.backend.helpers.setting import Setting
from yeksatr.backend.orm.model import *
from crawler.feed.newsagent import NewsAgent
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.helpers.email import sendmail


class BulletinAgent(object):
    '''
    Sends Bulletin to users
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def action(self):
        self.read_all_bulletin()
    
    def read_all_bulletin(self):
        query = (BulletinFilter.select(User.username,User.id,BulletinFilter.query_text,BulletinFilter.scan_period,
                                       BulletinFilter.fk_source.alias('source'),BulletinFilter.starred,Source.title)
                 .join(Source,JOIN_LEFT_OUTER).switch(BulletinFilter).join(Bulletin).join(User).naive())
        cnt = 0
        if query.count() > 0 :
            nw = NewsWorker()
           
            for row in query.execute():
                
                email = row.username
                user_id = row.id
                query_text = row.query_text
                scan_period = row.scan_period
                source = row.source
                starred = row.starred
                source_title = row.title
                
                title = "خبرنامه:";
                if source != None :
                    title += " {0} ".format(source_title)
                else:
                    title += " کل اخبار ";
                
                if scan_period != None:
                    title += " در {0} روز گذشته".format(scan_period)
                
                if starred != None :
                    title += " در موارد ستاره دار "
                
                if query_text != None:
                    title += " خبرهای شامل عبارت: "+query_text
                html = '''<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
                            <center>
                            <h2>یکسطر: درجریان باشید</h2>
                            <h2>''' +title+  '''</h2>
                            <div class="" style="direction:rtl;text-align:right;font-family:Tahoma;font-size:15px;width:650px; font: normal 12px/150% Tahoma; background: #fff; overflow: hidden; border: 1px solid #006699; -webkit-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; " >
                            <table style="border-collapse: collapse; text-align: right; width: 100%;" ><tbody>''';
                
                #print(user_id,email,source   )
                
               
                
                
                news = nw.get_news(query_text, source, scan_period, starred, user_id, 0, 100)
                
                for index,item in enumerate( news):
                    css_style = '''line-height:20px;font-family:Tahoma;padding: 3px 10px; color: #00496B; border-left: 1px solid #E1EEF4;font-size: 12px;font-weight: normal;
                                    '''
                    if index %2 == 0:
                        css_style += 'background: #E1EEF4; color: #00496B;'
                    
                        
                    html += """<tr>
                                    <td style='border-left: none;width:24px;{0}'><img style='width:16px;height:16px' src='http://yeksatr.com/{1}'</td>
                                    <td style='{0}' ><a style='text-decoration:none; color:black;cursor:pointer' href='{2}' target='_blank' >{3}</a></td>
                                    <td  style='width:80px;{0}' >{4}</td>                                    
                                </tr>""".format(css_style,item.icon,item.link,item.title,item.persian_date)
                html += "</tbody></table></div></center>" 
                sendmail(email, title, "", html)
                cnt+=1
                #file = open("c:\\temp\\1.html", mode='w', encoding="utf-8") 
                #file.write(html);
                #file.flush();
                #file.close();
                    
                    
                #print (len(news))
        print (str(cnt) +  " bulletin sent ")    
                
        pass
    
    
    def send_bulletin(self,html,title,email):
        pass