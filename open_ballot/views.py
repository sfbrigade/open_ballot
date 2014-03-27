import logging
import os
import subprocess

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession, BallotMeasure
    )

BUILD_DIR = 'build'

logger = logging.getLogger(__name__)

class BaseView(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='open_ballot', renderer='templates/index.pt')
    def my_view(self):
        return {'one': 'one', 'project': 'open_ballot'}

def app(request):
    logger.info('Building app...')
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    subprocess.call(['browserify',
                     'open_ballot/js/app.js',
                     '-o', 'build/bundle.js'])
    return FileResponse('build/bundle.js', request=request)

class BallotAjaxView(BaseView):
    @view_config(route_name='ajax_get_ballots', renderer='json',
        request_method='GET')
    def get_ballots(self):
        ballot_measure_jsons = []

        for ballot_measure in BallotMeasure.all():
            ballot_measure_json = {
                'id': ballot_measure.id,
                'prop_id': ballot_measure.prop_id,
                'description': ballot_measure.description,
                'num_yes': ballot_measure.num_yes,
                'num_no': ballot_measure.num_no,
                'passed': ballot_measure.passed,
                'election': {
                    'date': ballot_measure.election.date.isoformat()
                }
            }

            if ballot_measure.ballot_type:
                ballot_measure_json.update({'ballot_type': {
                    'name': ballot_measure.ballot_type.name,
                    'percent_required':\
                        float(ballot_measure.ballot_type.percent_required)
                    }
                }
            )

            ballot_measure_jsons.append(ballot_measure_json)

        return ballot_measure_jsons