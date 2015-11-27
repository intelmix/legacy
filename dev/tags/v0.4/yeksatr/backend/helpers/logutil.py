'''
Created on Feb 15, 2013

@author: root
'''


import os,datetime,time,sys,traceback
#from yeksatr.backend.setting import Setting
class LogUtil(object):
    '''
    classdocs
    '''


    def __init__(self,address,enable,debuging):        
        path =  address.replace(os.path.basename(address),"")
        if os.path.isdir(path)== False:            
            os.makedirs(path)
        self.file = open(address,"a+")
        self.enable = enable
        self.debuging = debuging
         
        
    def WriteLog(self,mess):
        if self.debuging:
            print (mess)
            #traceback.print_exc(file=sys.stdout)
        if self.enable:
            #print mess
            self.file.write(self.GetTime() + mess +"\r\n")
            self.file.flush()
            #traceback.print_exc(file=sys.stdout)
            
    def LogException(self,ex,title='This error occured! :'): 
        self.WriteLog(title+' ' +ex.__str__())  
           
        
    def GetTime(self):
        now =  datetime.datetime.now()        
        return str(now.year) +"/"+ str(now.month) +"/"+ str(now.day) +" "+ str(now.hour) +":"+ str(now.minute) +":"+ str(now.second)+" "
  
        
        
