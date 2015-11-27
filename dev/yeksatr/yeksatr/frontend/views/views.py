# coding: utf-8
# -*- coding: utf-8 -*-
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
                query = ""
                days = None
                source=None
                starred = None
                alert_message = ""
                if 'q' in request.params:
                    query = request.params.getone('q')
                
                if 'date' in request.params:
                    days = request.params.getone('date')
                
                if 'source' in request.params:
                    source = request.params.getone('source')
                if 'starred' in request.params:
                    tmp = request.params.getone('starred')
                    if tmp == 'true':
                        starred = True
                    else:
                        starred = False
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
                else:
                        if len(query) > 0 or days != None or source != None:
                            query = ""
                            days = None
                            source = None
                            alert_message = u'تنها کاربران عضو قادر به جستجو می باشند';
                if 'forgotPasswordKey' in request.params.keys():
                        forgot_key = request.params.getone('forgotPasswordKey')

                nw = NewsWorker()
                news = nw.get_news(query,source,days,starred,session['user_id'] if 'user_id' in session else None)    
                sources = nw.get_all_sources()         
                return  {'news':news,'authenticated':authenticated,'user_name':user_name,'forgot_key':forgot_key,
                         'search_text':query,'search_source':source,'search_date':days,'alert_message':alert_message,
                         'sources':sources,'starred':'true' if starred== True else 'false'}
        except Exception as ex:
                Setting.log.log_exception(ex)
                if Setting.debuging:
                        return Response(ex.__str__())
                else:
                        return Response('sorry,problem')

@view_config(route_name='api' , request_method='POST',renderer='json' )
def api(request):
        return manage_api(request)       
        pass

@view_config(route_name='apa' , request_method='GET',renderer='json' )
def apa(request):
        return manage_api(request)       
        pass
    
@notfound_view_config()
def not_found(request):
        return render_to_response('../templates/404.pt',{},request=request)
