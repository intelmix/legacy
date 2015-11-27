# -*- coding: utf-8 -*-
import configparser
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from yeksatr.frontend.views.views import *
from yeksatr.backend.helpers.setting import init_setting,test

def main(global_config, **settings):
    config_path = global_config['__file__']
    app_info = configparser.ConfigParser()
    app_info.read(config_path)        
    init_setting(app_info)
    
    config = Configurator(settings=settings)
    
    config.include('pyramid_chameleon')
    config.add_static_view(name='static', path= 'static', cache_max_age=0)  

    config.add_route('home', '/')    
    config.add_route('api','/api/{func}')   
    
    ys_session_factory = SignedCookieSessionFactory("thisissecretkay")
    config.set_session_factory(ys_session_factory)

    config.scan()
    return config.make_wsgi_app()
