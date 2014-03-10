import logging
import os
import subprocess

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

BUILD_DIR = 'build'

logger = logging.getLogger(__name__)

@view_config(route_name='open_ballot', renderer='templates/index.pt')
def my_view(request):
    return {'one': 'one', 'project': 'open_ballot'}

def app(request):
    logger.info('Building app...')
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    subprocess.call(['browserify',
                     'open_ballot/js/app.js',
                     '-o', 'build/bundle.js'])
    return FileResponse('build/bundle.js', request=request)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_open_ballot_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

