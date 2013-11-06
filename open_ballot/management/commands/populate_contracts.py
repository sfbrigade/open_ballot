from django.core.management.base import BaseCommand, CommandError
import csv, re, os
from configparser import ConfigParser
from dateutil import parser
from datetime import date

from open_ballot.models import (BallotMeasure, Committee, Stance,
    Consultant, Service, Contract, Election)

class Command(BaseCommand):
    args = '< filename >'
    help = """
    Input a CSV file from SFEthics.org, and optionally a .ini settings
    file.  This defines the CSV headers and maps them to attributes
    of our models.

    This is mostly intended for the contract data provided by Adrian.  It may
    not be reusable.
    """

    def handle(self, filename, settings=None, *args, **kwargs):
        if not filename.endswith('.csv'):
            raise Exception('Please input a csv file.')            
        #os.getcwd() gives the current directory that this
        #script is being run from
        #This way, the file's path can be accurately determined
        csv_file_path = os.path.join(os.getcwd(), filename)

        if settings:
            if not settings.endswith('.ini'):
                raise Exception('Settings must be a .ini file.')

            settings_file = os.path.join(os.getcwd(), settings)
        else:
            settings_file = os.path.join(os.path.dirname(__file__), 'headers.ini')


        #Open config file to get the csv headers to properly
        #parse the csv file
        configparser = ConfigParser()
        configparser.read_file(open(settings_file))

        headers = {
        'committee_name': configparser.get('contracts', 'committee_name'),
        'stance': configparser.get('contracts', 'stance'),
        'election_date': configparser.get('contracts', 'election_date'),
        'prop_id': configparser.get('contracts', 'prop_id'),
        'consultant': configparser.get('contracts', 'consultant'),
        'service': configparser.get('contracts', 'service'),
        'payment': configparser.get('contracts', 'payment')
        }

        reader = csv.DictReader(open(csv_file_path))

        for row in reader:
            try:
                if len(row[headers['prop_id']]) > 3:
                    continue

                if row[headers['committee_name']]:
                    CurrentElection.set_committee(row[headers['committee_name']])

                if row[headers['election_date']] and row[headers['prop_id']]:
                    CurrentElection.set_ballot_measure(
                        row[headers['election_date']],
                        row[headers['prop_id']]
                    )

                if not CurrentElection.election or \
                    (CurrentElection.election and\
                    not CurrentElection.election.is_valid()):
                    continue

                if row[headers['stance']]:
                    voted_yes = row[headers['stance']].lower().strip() == 'yes'
                    Stance.get_or_create(committee=CurrentElection.committee,
                        ballot_measure=CurrentElection.ballot_measure,
                        voted_yes=voted_yes)

                if row[headers['consultant']]:
                    #TODO: Should we change this from last_name to something else?
                    #Are consultants ever independents?
                    consultant = Consultant.get_or_create(
                        name=row[headers['consultant']]
                        )

                    payment = row[headers['payment']]\
                        .strip().replace('$', '').replace(',', '')

                    try:
                        payment = float(payment)
                    except ValueError:
                        payment = 0

                    contract = Contract.get_or_create(
                        consultant=consultant,
                        committee=CurrentElection.committee,
                        payment=payment,
                        service_description=row[headers['service']]
                        )
            except:
                import ipdb;ipdb.set_trace()
                raise

class CurrentElection(object):
    ballot_measure = None
    committee = None

    @staticmethod
    def set_ballot_measure(election_date, prop_id):
        election = Election.get_or_create(election_date)
        ballot_measure = BallotMeasure.get_or_create(
            election=election, prop_id=prop_id)
        CurrentElection.ballot_measure = ballot_measure

    @staticmethod
    def set_committee(committee_name):
        if committee_name not in ('', 'N/A'):
            committee = Committee.get_or_create(name=committee_name)
            CurrentElection.committee = committee