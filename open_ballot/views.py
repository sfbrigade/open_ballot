import logging
import os
import subprocess

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import and_

from .models import (
    DBSession, BallotMeasure, Committee, Contract, Stance
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
    @view_config(route_name='ajax_get_ballot', renderer='json',
        request_method='GET')
    def get_ballot(self):
        '''
        Returns a single ballot.  Called with GET /ajax/ballots/{id}
        Note that some ballot measures are missing a ballot type.
        '''

        ballot_measure = BallotMeasure.get_by_id(self.request.matchdict['id'])
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

        return ballot_measure_json

    @view_config(route_name='ajax_get_ballots', renderer='json',
        request_method='GET')
    def get_ballots(self):
        '''
        Returns a list of all ballots.  Called with GET /ajax/ballots
        Note that some ballot measures are missing a ballot type.
        '''

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

    @view_config(route_name='ajax_get_donations', renderer='json',
        request_method='GET')
    def get_committees(self):
        '''
        Get the committees working on a ballot measure, with their stance.
        Called by GET /ajax/ballots/{id}/committees
        '''
        committee_jsons = []

        ballot_measure = BallotMeasure.get_by_id(self.request.matchdict['id'])
        committees = DBSession.query(Committee).join(
            Stance, and_(
                Stance.ballot_measure_id==ballot_measure.id,
                Stance.committee_id==Committee.id)
            ).join(
                Contract, and_(
                    Contract.committee_id==Committee.id
                )
            )

        for committee in committees:
            # Sum the contracts
            total_spend = sum(map(lambda contract: contract.payment,
                committee.contracts))

            committee_json = {
                'id': committee.id,
                'name': committee.name,
                'election': {
                    'date': committee.election.date.isoformat()
                },
                'stance': {
                    #TODO: Rename this to "supported"?
                    'voted_yes': committee.stance.voted_yes
                },
                'total_spend': total_spend
            }

            committee_jsons.append(committee_json)

        return committee_jsons
