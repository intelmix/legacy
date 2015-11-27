'''
Created on May 29, 2014

@author: hossein
'''
from yeksatr.backend.helpers.setting import Setting
from .model import User
from _datetime import datetime
from yeksatr.backend.helpers.utility import *

class UserWorker(object):

    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def SignUp(self,email,username,password):
        cnt = User.select().where( (User.email == email) | (User.username == username)).count()
        if cnt == 0:
            u = User(email=email,username=username,password=password,register_date=datetime.now())
            u.save()
            return True
        else:
            return False
        
        print (cnt)
        return True
        pass

    def SignIn(self,username,password):
        query = User.select().where( (User.password == password) & (User.username == username))
        
        if query.count() == 1:
            res = query.execute();
            for item in res:
                if item.name == None and item.familly == None:
                    name = item.username
                else:
                    name = item.name or '' + ' ' + item.familly or ''
                
                
                return (True,name)
            
        return (False)
    
    def GetUserFullName(self,username):
        query = User.select().where(User.username==username)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                if item.name == None and item.familly == None:
                    return item.username
                else:
                    return item.name or '' + ' ' + item.familly or ''
        return ""
                
        

    
        
