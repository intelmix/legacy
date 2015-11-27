from pyramid.response import Response
from yeksatr.backend.helpers.utility import *
from yeksatr.backend.helpers.logutil import LogUtil
from yeksatr.backend.helpers.setting import Setting,InitDB
from yeksatr.backend.orm.user import UserWorker
import datetime
from yeksatr.backend.orm.model import *
import requests


def ManageApi(request):
    Setting.log.LogRequest(request)
    func = request.matchdict['func']
    if func == 'SignUp':
        return SignUp(request)
        pass
    elif func == 'SignIn':
        return SignIn(request)
        pass
    elif func == 'LogOut':
        return LogOut(request)
        pass
    elif func == 'Feedback':
        return feedback(request)
        pass
    else:
        Setting.log.info("invalid api request:"+func)
    
    
def SignUp(request):
    try:
        success = False
        fail_type = ''
        
        if request.POST.has_key('email') and request.POST.has_key('username') and request.POST.has_key('password') :
            Setting.log.info('signup attemp for email: '+request.POST['email']+" , username:"+request.POST['username'])
            captchaVerificationUrl = 'http://www.opencaptcha.com/validate.php?ans='+request.POST['captchaText']+'&img='+request.POST['captchaImg']
            Setting.log.info('starting captcha test for '+captchaVerificationUrl)
            r = requests.get(captchaVerificationUrl)
            captchaResult = r.text   #this will be either 'pass' or 'fail' if it is fail then captcha is rejected

            Setting.log.info('captcha check result is '+captchaResult)
            if ( captchaResult == 'fail'):
                fail_type = 'captcha'
                
            if ( captchaResult == 'pass' ):
                uw = UserWorker()
                InitDB()
                if uw.SignUp(request.POST['email'], request.POST['username'], request.POST['password']):
                    success = True
                    Setting.log.info('signup done for email: '+request.POST['email']+" , username:"+request.POST['username'])
                else:
                    fail_type = 'data'
                
                    
        return {'success':success, 'fail_type': fail_type}
    except Exception as ex:
        Setting.log.LogException(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
        
def SignIn(request):
    try:
        success = False
        if request.POST.has_key('username') and request.POST.has_key('password') :
            Setting.log.info("login attemp for user:"+request.POST['username'])
            uw = UserWorker()
            InitDB()
            res = uw.SignIn(request.POST['username'], request.POST['password'])
            if res[0] :
                request.session['authenticated'] =  True 
                request.session['username'] = request.POST['username']
                request.session['user_id' ] = res[2]
                Setting.log.info('sign in done for '+res[1]+' and user id is '+str(res[2]))
                return {'success':True,'name':res[1]}   
                
        return {'success':success}
    except Exception as ex:
        Setting.log.LogException(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
        
def LogOut(request):   
    try:          
        Setting.log.info("logging out user:"+request.session['username']) 
        request.session['authenticated'] =  False 
        request.session['username'] = ""
               
        return {'success':True}        
    except Exception as ex:
        Setting.log.LogException(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
    

def feedback(request):
    try:
        InitDB()
        content = request.POST['txtFeedback']
        Setting.log.info('inserting feedback '+content)
        fk_user = None
        if ( request.session['user_id'] != None ):
            fk_user = request.session['user_id']
            Setting.log.info('feedback is from signed in user with id='+str(fk_user))
                    
        feedbackRecord = Feedback(contents = content, fk_user = fk_user, submit_date = datetime.datetime.now());                
        feedbackRecord.save()
        Setting.log.info('insert feedback done')
        return {}
    except Exception as ex:
        Setting.log.LogException(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
