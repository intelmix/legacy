from pyramid.config import Configurator
import configparser
from pyramid.session import SignedCookieSessionFactory
from yeksatr.frontend.views.views import *
from yeksatr.backend.helpers.setting import InitSetting
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config_path = global_config['__file__']
    config = configparser.ConfigParser()
    config.read(config_path)
    mode = config.get('app:main','mode')
    print (mode)
    InitSetting(mode)
    #db_url = config.get('app:main', 'sqlalchemy.url')
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view(name='static', path= 'static', cache_max_age=0)
    config.add_static_view(name='website', path= '../website', cache_max_age=0)
  
    config.add_route('test', '/test')
    config.add_route('home', '/')
    
  
    config.add_route('UpdateNews','/UpdateNews')
    config.add_route('ExtractNews','/ExtractNews')
    config.add_route('inn','/inn/{one}/{two}')
    
    config.add_route('SignUp','/SignUp')
    config.add_route('SignIn','/SignIn')
    config.add_route('LogOut','/LogOut') 
  
    
    ys_session_factory = SignedCookieSessionFactory("thisissecretkay")
    config.set_session_factory(ys_session_factory)

    config.scan()
    return config.make_wsgi_app()
