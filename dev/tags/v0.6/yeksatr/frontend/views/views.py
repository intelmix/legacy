import sys,traceback
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response



from yeksatr.backend.helpers.utility import *
from yeksatr.backend.helpers.logutil import LogUtil
from yeksatr.backend.helpers.setting import Setting,InitDB
from yeksatr.backend.feed.rssreader import RssReader
from yeksatr.backend.orm.news import NewsWorker
from yeksatr.backend.feed.newsagent import NewsAgent
from yeksatr.backend.orm.user import UserWorker
from yeksatr.api.controller import ManageApi

#Setting.log.info("starting app")



@view_config(route_name='UpdateNews')
def UpdateNews(request):
	try:
		InitDB()
		rr = RssReader()
		return Response( "res is "+str(rr.Read() ))
	except Exception as ex:
		Setting.log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')

@view_config(route_name='ExtractNews')
def ExtractNews(request):    
	try:
		InitDB()
		na = NewsAgent()    
		return Response( "res is "+str(na.ExtractNews(30) ))
	except Exception as ex:
		Setting.log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')
		
@view_config(route_name='home', renderer='../templates/index.pt')
def HomePage(header,request):	
	#raise()
	Setting.log.LogRequest(request)
	try:
		#LogOut(header,request)
		InitDB()
		user_name = ""
		authenticated = False
		session = request.session
		if 'authenticated' in session and session['authenticated']:
			authenticated = True
			uw = UserWorker()			
			user_name = uw.GetUserFullName(session['username'])
			
		rr = RssReader()
		rr.Read()	
		nw = NewsWorker()
		news = nw.GetNews()		
		return {'news':news,'authenticated':authenticated,'user_name':user_name}
	except Exception as ex:
		Setting.log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')

@view_config(route_name='test', renderer='../templates/test.pt')
def TestPage(header,request):	
	Setting.log.error("error")
	Setting.log.info("info")
	Setting.log.debug("debug ")
	return {}


@view_config(route_name='api' , request_method='POST',renderer='json' )
def Api(request):
	return ManageApi(request)	
	pass

	


@notfound_view_config()
def NotFound(request):
	return render_to_response('../templates/404.pt',{},request=request)

