import random
import string
from datetime import datetime
import requests
from pyramid.response import Response
from yeksatr.backend.helpers.utility import *
from yeksatr.backend.helpers.logutil import LogUtil
from yeksatr.backend.helpers.setting import Setting,init_db
from yeksatr.backend.orm.user import UserWorker
from yeksatr.backend.helpers.email import *
from yeksatr.backend.orm.model import *

def manage_api(request):
    Setting.log.log_request(request)
    func = request.matchdict['func']
    if func == 'SignUp':
        return sign_up(request)
        pass
    elif func == 'SignIn':
        return sign_in(request)
        pass
    elif func == 'SignOut':
        return sign_out(request)
        pass
    elif func == 'Feedback':
        return feedback(request)
        pass
    elif func == 'ForgotPassword':
        return forgot_password(request)
        pass
    elif func == 'ResetPassword':
        return reset_password(request)
        pass
    else:
        Setting.log.info("invalid api request:"+func)

    
def reset_password(request):
    try:
        success = False
        if request.POST.has_key('resetKey'):
            reset_key = request.POST['resetKey']
            
            Setting.log.info("Reset password attemp for key:"+reset_key)
            uw = UserWorker()
            init_db()
            username = uw.find_username_by_reset_password_key(reset_key)
            email = uw.get_user_email(username)
            if email != "":
                Setting.log.info("Reset password attemp for user:"+username +' found email:'+email)
                #generate a unique random reference string
                new_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
                uw.do_reset_password(username, new_password)
                
                Setting.log.info("user password changed to "+new_password)

                (title, text, html) = get_reset_password_template()

                text = text.format(new_password)
                html = html.format(new_password)
                
                Setting.log.info("got template - title is "+title)
                sendmail(email, title, text, html)
                Setting.log.info("mail sent to "+email)
                success = True
                
    except Exception as ex:
        Setting.log.log_exception(ex)

    return { 'success': success}
    

def forgot_password(request):
    try:
        success = False
        if request.POST.has_key('username'):
            username = request.POST['username']
            
            Setting.log.info("Forgot password attemp for user:"+username)
            uw = UserWorker()
            init_db()
            email = uw.get_user_email(username)
            if email != "":
                Setting.log.info("Forgot password attemp for user:"+username +' found email:'+email)
                #generate a unique random reference string
                reset_password_key = 'f'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(31))
                reset_password_request_date = datetime.datetime.now()
                Setting.log.info("Forgot password attemp for user:"+username +' reset key is:'+reset_password_key)
                uw.update_password_reset_info(username, reset_password_key, reset_password_request_date)
                
                Setting.log.info("receiving email template")
                (title, text, html) = get_forgot_password_template()

                site_prefix = "www"
                if ( Setting.mode == "beta" ):
                    site_prefix="beta"
                    
                text = text.format("http://"+site_prefix+".yeksatr.com/?forgotPasswordKey="+reset_password_key)
                html = html.format("http://"+site_prefix+".yeksatr.com/?forgotPasswordKey="+reset_password_key)
                
                Setting.log.info("got template - title is "+title)
                sendmail(email, title, text, html)
                Setting.log.info("mail sent to "+email)
                
    except Exception as ex:
        Setting.log.log_exception(ex)

    return Response('')

            
def sign_up(request):
    try:
        success = False
        fail_type = ''
        
        if request.POST.has_key('email') and request.POST.has_key('username') and request.POST.has_key('password') :
            Setting.log.info('signup attemp for email: '+request.POST['email']+" , username:"+request.POST['username'])
            captcha_verification_url = 'http://www.opencaptcha.com/validate.php?ans='+request.POST['captchaText']+'&img='+request.POST['captchaImg']
            Setting.log.info('starting captcha test for '+captcha_verification_url)
            r = requests.get(captcha_verification_url)
            captcha_result = r.text   #this will be either 'pass' or 'fail' if it is fail then captcha is rejected

            Setting.log.info('captcha check result is '+captcha_result)
            if ( captcha_result == 'fail'):
                fail_type = 'captcha'
                
            if ( captcha_result == 'pass' ):
                uw = UserWorker()
                init_db()
                if uw.sign_up(request.POST['email'], request.POST['username'], request.POST['password']):
                    success = True
                    Setting.log.info('signup done for email: '+request.POST['email']+" , username:"+request.POST['username'])
                else:
                    fail_type = 'data'
                
                    
        return {'success':success, 'fail_type': fail_type}
    except Exception as ex:
        Setting.log.log_exception(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
        
def sign_in(request):
    try:
        success = False
        if request.POST.has_key('username') and request.POST.has_key('password') :
            Setting.log.info("login attemp for user:"+request.POST['username'])
            uw = UserWorker()
            init_db()
            res = uw.sign_in(request.POST['username'], request.POST['password'])
            if res[0] :
                request.session['authenticated'] =  True 
                request.session['username'] = request.POST['username']
                request.session['user_id' ] = res[2]
                Setting.log.info('sign in done for '+res[1]+' and user id is '+str(res[2]))
                return {'success':True,'name':res[1]}   
                
        return {'success':success}
    except Exception as ex:
        Setting.log.log_exception(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
        
def sign_out(request):   
    try:          
        Setting.log.info("signing out user:"+request.session['username']) 
        request.session['authenticated'] =  False 
        request.session['username'] = ""
        return {'success':True}        
    except Exception as ex:
        Setting.log.log_exception(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')
    

def feedback(request):   
    try:
        init_db()
        content = request.POST['txtFeedback']
        Setting.log.info('inserting feedback '+content)
        fk_user = None
        
        if ('user_id' in request.session and  request.session['user_id'] != None ):
            fk_user = request.session['user_id']
            Setting.log.info('feedback is from signed in user with id='+str(fk_user))
                    
        feedback_record = Feedback(contents = content, fk_user = fk_user, submit_date = datetime.now());                
        feedback_record.save()
        Setting.log.info('insert feedback done')
        return {}
    except Exception as ex:
        Setting.log.log_exception(ex)
        if Setting.debuging:
            return Response(ex.__str__())
        else:
            return Response('sorry,problem')

            
