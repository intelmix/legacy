import sys,traceback
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from yeksatr.backend.helpers.utility import *
from yeksatr.backend.helpers.logutil import LogUtil
from yeksatr.backend.helpers.setting import Setting,init_db
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.orm.user import UserWorker
from yeksatr.api.controller import manage_api

@view_config(route_name='home', renderer='../templates/index.pt')
def home_page(header,request):   
        #raise()
        Setting.log.log_request(request)
        try:
                forgot_key = None
                #LogOut(header,request)
                init_db()
                user_name = ""
                authenticated = False
                session = request.session
                if 'authenticated' in session and session['authenticated']:
                        authenticated = True
                        uw = UserWorker()                       
                        user_name = uw.get_user_full_name(session['username'])
                if 'forgotPasswordKey' in request.params.keys():
                        forgot_key = request.params.getone('forgotPasswordKey')

                nw = NewsWorker()
                news = nw.get_news()             
                return {'news':news,'authenticated':authenticated,'user_name':user_name,'forgot_key':forgot_key}
        except Exception as ex:
                Setting.log.log_exception(ex)
                if Setting.debuging:
                        return Response(ex.__str__())
                else:
                        return Response('sorry,problem')

@view_config(route_name='test', renderer='../templates/test.pt')
def test_page(header,request):   
        Setting.log.error("error")
        Setting.log.info("info")
        Setting.log.debug("debug ")
        return {}

@view_config(route_name='api' , request_method='POST',renderer='json' )
def api(request):
        return manage_api(request)       
        pass

@notfound_view_config()
def not_found(request):
        return render_to_response('../templates/404.pt',{},request=request)
