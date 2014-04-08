from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )
import api_urls

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(name='js/thirdparty', path='open_ballot:js/thirdparty')
    config.add_static_view(name='partials', path='open_ballot:partials')
    config.add_static_view(name='data', path='../data')

    config.add_route('open_ballot', '/')

    for ListClass in api_urls.ListUrl.__subclasses__():
        config.add_route(ListClass.get_list_route(), ListClass.get_list_url())

    for ResourceClass in api_urls.ResourceUrl.__subclasses__():
        config.add_route(ResourceClass.get_resource_route(),
            ResourceClass.get_routing_url())

    config.add_route('app', '/js/app.js')
    config.add_view('open_ballot.views.app', route_name='app')

    config.scan()
    return config.make_wsgi_app()
