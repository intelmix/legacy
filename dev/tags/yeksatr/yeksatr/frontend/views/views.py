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

Setting.error_log = LogUtil(Setting.main_log_path,Setting.log_enable,Setting.debuging)
Setting.error_log.WriteLog("starting app")


	
@view_config(route_name='inn')
def index2(request):
	return Response(PrettyDate(10800))

@view_config(route_name='UpdateNews')
def UpdateNews(request):
	try:
		InitDB()
		rr = RssReader()
		return Response( "res is "+str(rr.Read() ))
	except Exception as ex:
		Setting.error_log.LogException(ex)
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
		Setting.error_log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')
@view_config(route_name='home', renderer='../templates/index.pt')
def HomePage(header,request):	
	print("ff")
	try:
		#LogOut(header,request)
		InitDB()
		user_name = ""
		authenticated = "false"
		session = request.session
		if 'authenticated' in session and session['authenticated']:
			authenticated = "true"
			uw = UserWorker()			
			user_name = uw.GetUserFullName(session['username'])
			
		rr = RssReader()
		rr.Read()	
		nw = NewsWorker()
		news = nw.GetNews()		
		return {'news':news,'authenticated':authenticated,'user_name':user_name}
	except Exception as ex:
		Setting.error_log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')

@view_config(route_name='test', renderer='../templates/test.pt')
def TestPage(header,request):
	
	return {}


@view_config(route_name='SignUp' , request_method='POST',renderer='json' )
def SignUp(header,request):
	try:
		success = False
		if request.POST.has_key('email') and request.POST.has_key('username') and request.POST.has_key('password') :
			uw = UserWorker()
			InitDB()
			if uw.SignUp(request.POST['email'], request.POST['username'], request.POST['password']):
				success = True
		
		return {'success':success}
	except Exception as ex:
		Setting.error_log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')
		
@view_config(route_name='SignIn' , request_method='POST',renderer='json' )
def SignIn(header,request):
	try:
		success = False
		if request.POST.has_key('username') and request.POST.has_key('password') :
			uw = UserWorker()
			InitDB()
			res = uw.SignIn(request.POST['username'], request.POST['password'])
			if res[0] :
				request.session['authenticated'] =  True 
				request.session['username'] = request.POST['username']
				return {'success':True,'name':res[1]}	
				
		return {'success':success}
	except Exception as ex:
		Setting.error_log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')

 
@view_config(route_name='LogOut' , renderer='json' ) 
def LogOut(header,request):
	try:		
		request.session['authenticated'] =  False 
		request.session['username'] = ""
		return {'success':True}	
				
		
	except Exception as ex:
		Setting.error_log.LogException(ex)
		if Setting.debuging:
			return Response(ex.__str__())
		else:
			return Response('sorry,problem')
                       
                        


@notfound_view_config()
def NotFound(request):
	return render_to_response('../templates/404.pt',{},request=request)

