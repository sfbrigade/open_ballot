import logging
import os
import subprocess

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy import and_

from .models import (
    DBSession, BallotMeasure, Committee, Stance, Contract,
    Consultant, Donor, Donation
    )

import api_urls

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
    @view_config(route_name=api_urls.BallotUrl.get_list_route(), renderer='json',
        request_method='GET')
    def ballot_list(self):
        '''
        Returns a list of all ballot resources.  Called with GET /api/v1/ballots
        '''

        ballot_measure_jsons = []

        for ballot_measure in BallotMeasure.all():
            ballot_measure_json = {
                'id': ballot_measure.id,
                'prop_id': ballot_measure.prop_id,
                'name': ballot_measure.name,
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

            committees = DBSession.query(Committee).join(
                Stance, and_(
                    Stance.ballot_measure_id==ballot_measure.id,
                    Stance.committee_id==Committee.id)
                ).join(
                    Contract, and_(
                        Contract.committee_id==Committee.id
                    )
                )

            ballot_measure_json['committees'] = []
            for committee in committees:
                ballot_measure_json['committees'].append({
                    'id': committee.id,
                    'name': committee.name,
                    'resource':\
                        api_urls.CommitteeUrl.get_resource_url(committee.id)
                })

            ballot_measure_jsons.append(ballot_measure_json)

        return ballot_measure_jsons

    @view_config(route_name=api_urls.BallotUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def ballot_resource(self):
        '''
        Returns the fields of a ballots.  Called with GET /api/v1/ballots/{id}
        Note that some ballot measures are missing a ballot type.
        '''

        ballot_measure = BallotMeasure.get_by_id(self.request.matchdict['id'])
        if not ballot_measure:
            return HTTPNotFound

        ballot_measure_json = {
            'id': ballot_measure.id,
            'prop_id': ballot_measure.prop_id,
            'name': ballot_measure.name,
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

        committees = DBSession.query(Committee).join(
            Stance, and_(
                Stance.ballot_measure_id==ballot_measure.id,
                Stance.committee_id==Committee.id)
            ).join(
                Contract, and_(
                    Contract.committee_id==Committee.id
                )
            )

        ballot_measure_json['committees'] = []
        for committee in committees:
            ballot_measure_json['committees'].append({
                'id': committee.id,
                'name': committee.name,
                'resource':\
                    api_urls.CommitteeUrl.get_resource_url(committee.id)
            })

        return ballot_measure_json

    # @view_config(route_name=api_urls.CommitteeUrl.get_list_route(),
    #     renderer='json', request_method='GET')
    # def get_committee_list(self):
    #     '''
    #     Get the committees working on a ballot measure, with their stance.
    #     Called by GET /api/v1/committees
    #     '''
    #     committee_jsons = []

    #     ballot_measure = BallotMeasure.get_by_id(self.request.matchdict['id'])
    #     committees = DBSession.query(Committee).join(
    #         Stance, and_(
    #             Stance.ballot_measure_id==ballot_measure.id,
    #             Stance.committee_id==Committee.id)
    #         )

    #     for committee in committees:
    #         committee_json = {
    #             'id': committee.id,
    #             'name': committee.name,
    #             'election': {
    #                 'date': committee.election.date.isoformat()
    #             },
    #             'stance': {
    #                 #TODO: Rename this to "supported"?
    #                 'voted_yes': committee.stance.voted_yes
    #             },
    #             'resource':\
    #                 api_urls.CommitteeUrl.get_resource_url(committee.id)
    #         }

    #         committee_jsons.append(committee_json)

    #     return committee_jsons

    @view_config(route_name=api_urls.CommitteeUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def get_committee_resource(self):
        '''
        Get a committee working on a ballot measure, with their stance.
        Called by GET /api/v1/committees/{id}
        '''
        committee = Committee.get_by_id(self.request.matchdict['id'])

        committee_json = {
            'id': committee.id,
            'name': committee.name,
            'donation_total': committee.donation_total,
            'total_spent': committee.total_spent,
            'election': {
                'date': committee.election.date.isoformat()
            },
        }

        committee_json['ballot_measures'] = []
        for stance in committee.stances:
            committee_json['ballot_measures'].append({
                'id': stance.ballot_measure_id,
                'name': stance.ballot_measure.name,
                'resource':\
                    api_urls.BallotUrl.get_resource_url(
                        stance.ballot_measure_id
                        ),
                'stance': {
                    'voted_yes': stance.voted_yes
                }
                })

        committee_json['contracts'] = []
        for contract in committee.contracts:
            committee_json['contracts'].append({
                'id': contract.id,
                'description': contract.description,
                'resource': api_urls.ContractUrl.get_resource_url(contract.id)
            })

        committee_json['donations'] = []
        for donation in committee.donations:
            committee_json['donations'].append({
                'id': donation.id,
                'amount': donation.amount,
                'resource': api_urls.DonationUrl.get_resource_url(donation.id)
            })

        return committee_json

    @view_config(route_name=api_urls.ContractUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def get_contract_resource(self):
        '''
        Returns details for a consultant's contract to perform some
        services for a committee

        GET /api/v1/contracts/{id}
        '''

        contract = Contract.get_by_id(self.request.matchdict['id'])
        contract_json = {
            'id': contract.id,
            'description': contract.description,
            'payment': contract.payment
        }

        consultant = contract.consultant

        contract_json['consultant'] = {
            'id': consultant.id,
            'name': consultant.name,
            'resource': api_urls.ConsultantUrl.get_resource_url(consultant.id)
        }

        committee = contract.committee

        contract_json['committee'] = {
            'id': committee.id,
            'name': committee.name,
            'resource':\
                api_urls.CommitteeUrl.get_resource_url(committee.id)
        }

        return contract_json

    @view_config(route_name=api_urls.ConsultantUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def get_consultant_resource(self):
        '''
        Returns details for a consultant, notably all contracts the consultant has
        signed.  Consultants' addresses will also be returned, unlike donors.

        GET /api/v1/contracts/{id}
        '''

        consultant = Consultant.get_by_id(self.request.matchdict['id'])

        consultant_json = {
            'id': consultant.id,
            'name': consultant.name,
            'address': consultant.address
        }

        consultant_json['contracts'] = []
        for contract in consultant.contracts:
            consultant_json['contracts'].append({
                'id': contract.id,
                'description': contract.description,
                'resource': api_urls.ContractUrl.get_resource_url(contract.id)
            })

        return consultant_json

    @view_config(route_name=api_urls.DonationUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def get_donation_resource(self):
        '''
        Information for a donation, including resource to the donor.

        GET /api/v1/donations/{id}
        '''

        donation = Donation.get_by_id(self.request.matchdict['id'])

        donation_json = {
            'id': donation.id,
            'amount': donation.amount,
            'transaction_date': donation.transaction_date.isoformat()
        }

        committee = donation.committee

        donation_json['committee'] = {
            'id': committee.id,
            'name': committee.name,
            'resource':\
                api_urls.CommitteeUrl.get_resource_url(committee.id)
        }

        donor = donation.donor
        donation_json['donor'] = {
            'id': donor.id,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
            'resource': api_urls.DonorUrl.get_resource_url(donor.id)
        }

        return donation_json

    @view_config(route_name=api_urls.DonorUrl.get_resource_route(),
        renderer='json', request_method='GET')
    def get_donor_resource(self):
        '''
        Gives details on a donor's donation history.  We will NOT be returning
        their employer or address at this time.

        GET /api/v1/donors/{id}
        '''

        donor = Donor.get_by_id(self.request.matchdict['id'])
        donor_json = {
            'id': donor.id,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
        }

        donor_json['donations'] = []
        for donation in donor.donations:
            donor_json['donations'].append({
                'id': donation.id,
                'amount': donation.amount,
                'resource': api_urls.DonationUrl.get_resource_url(donation.id)
            })

        return donor_json
