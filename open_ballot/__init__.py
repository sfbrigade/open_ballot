from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


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

    config.add_route('open_ballot', '/')

    config.add_route('app', '/js/app.js')
    config.add_view('open_ballot.views.app', route_name='app')

    config.scan()
    return config.make_wsgi_app()
