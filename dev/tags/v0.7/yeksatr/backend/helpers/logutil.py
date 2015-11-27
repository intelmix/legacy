'''
Created on Feb 15, 2013

@author: root
'''


import os,datetime,time,sys,traceback,logging
#from yeksatr.backend.setting import Setting
class LogUtil(object):
    '''
    classdocs
    '''
    log = None

    def __init__(self,path='',level=0,enable=True):
        self.enable = enable
        if self.enable :        
            dir_path =  path.replace(os.path.basename(path),"")
            if os.path.isdir(dir_path)== False:            
                os.makedirs(dir_path)
            
            self.log = logging.getLogger('')
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            error_handler = logging.FileHandler(path+'error.log')
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            self.log.addHandler(error_handler)
            
            if level >= 1 :
                info_handler = logging.FileHandler(path+'info.log')
                info_handler.setLevel(logging.INFO)
                info_handler.setFormatter(formatter)
                self.log.addHandler(info_handler)
                
            if level >= 2 :
                debug_handler = logging.FileHandler(path+'debug.log')
                debug_handler.setLevel(logging.DEBUG)
                debug_handler.setFormatter(formatter)
                self.log.addHandler(debug_handler)
                
            if level == 2 :
                self.log.setLevel(logging.DEBUG)
            elif level == 1:
                self.log.setLevel(logging.ERROR)
            else:
                self.log.setLevel(logging.INFO)
            
            self.enable = enable
            
    def info(self,message):
        self.log.info(message)
        pass
    
    def debug(self,message):
        self.log.debug(message)
        pass    
    
    def error(self,message):
        self.log.error(message,exc_info=True)
        pass     
            
    def log_exception(self,ex,title='This error occured! :'):  
        self.error(title+' ' +ex.__str__())
        #print(ex.__str__());
        #self.WriteLog(title+' ' +ex.__str__())  
              
    def log_request(self,request):
        mess = "url:" + request.url
        mess += "\nclient ip: "+request.remote_addr
        mess += "\nGET: "+str(request.GET)
        mess += "\nPOST: "+str(request.POST)
        self.info(mess)
        
    def get_time(self):
        now =  datetime.datetime.now()        
        return str(now.year) +"/"+ str(now.month) +"/"+ str(now.day) +" "+ str(now.hour) +":"+ str(now.minute) +":"+ str(now.second)+" "
