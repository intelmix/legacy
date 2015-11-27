'''
Created on May 29, 2014

@author: hossein
'''
from yeksatr.backend.helpers.setting import Setting
from .model import User
from datetime import datetime
from yeksatr.backend.helpers.utility import *

class UserWorker(object):
    def __init__(self):
        pass
    
    def sign_up(self,username,password):
        cnt = User.select().where(  User.username == username).count()
        if cnt == 0:
            u = User(username=username,password=password,register_date=datetime.now())
            u.save()
            return True
        else:
            return False
        
        print (cnt)
        return True
        pass

    def sign_in(self,username,password):
        query = User.select().where( (User.password == password) & (User.username == username))
        
        if query.count() == 1:
            res = query.execute();
            for item in res:
                id = item.id
                if item.name == None and item.familly == None:
                    name = item.username
                else:
                    name = item.name or '' + ' ' + item.familly or ''
                
                
                return (True,name, id)
            
        return (False,False,False)
    
    def get_user_full_name(self,username):
        query = User.select().where(User.username==username)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                if item.name == None and item.familly == None:
                    return item.username
                else:
                    return item.name or '' + ' ' + item.familly or ''
        return ""
                
    def get_user_email(self, username):
        query = User.select().where(User.username==username)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                return item.username
        return ""

    def update_password_reset_info(self, username, reset_password_key, reset_password_request_date):
        query = User.select().where(User.username==username)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                item.reset_password_key = reset_password_key
                item.reset_password_request_date = reset_password_request_date
                item.save()
                
    def find_username_by_reset_password_key(self, reset_key):
        query = User.select().where(User.reset_password_key==reset_key)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                return item.username
        return None
        
    def do_reset_password(self, username, new_password):
        query = User.select().where(User.username==username)
        if query.count() == 1:
            res = query.execute()
            for item in res:
                item.password = new_password
                item.reset_password_request_date = None
                item.reset_password_key = None
                item.save()
            
    def get_user_profile(self,user_id):
        query = User.select().where(User.id == user_id)
        if query.count() > 0:
            res = query.execute()
            for item in res:
                return item
        
    def set_user_profile(self,user_id,name,familly,mobile_number,password):
        query = User.select().where(User.id == user_id)
        if query.count() > 0:
            res = query.execute()
            for item in res:
                item.name = name
                item.familly = familly                
                item.mobile_number = mobile_number
                if password != None :
                    if len(password)>=6:
                        item.password = password
                item.save()
                return True
        return False
        