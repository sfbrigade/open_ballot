from django.core.management.base import BaseCommand, CommandError
import csv, re, os
from configparser import ConfigParser
from dateutil import parser
from datetime import date

from open_ballot.models import (BallotMeasure, Election, Tag, BallotType)

class Command(BaseCommand):
    args = '< filename >'
    help = """
    Input a CSV file and optionally a .ini settings
    file.  This defines the CSV headers and maps them to attributes
    of our models.

    This is mostly intended for the ballot measure data provided by Adrian.
    It may not be reusable.
    """

    def handle(self, filename, settings=None, *args, **kwargs):
        try:
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
            'issue': configparser.get('ballots', 'issue'),
            'prop_id': configparser.get('ballots', 'prop_id'),
            'name': configparser.get('ballots', 'name'),
            'election_date': configparser.get('ballots', 'election_date'),
            'description': configparser.get('ballots', 'description'),
            'passed': configparser.get('ballots', 'passed'),
            'num_votes': configparser.get('ballots', 'num_votes'),
            'percent_required': configparser.get('ballots', 'percent_required'),
            'type': configparser.get('ballots', 'type')
            }

            reader = csv.DictReader(open(csv_file_path))

            for row in reader:
                election = Election.get_or_create(row[headers['election_date']])

                if '' in [row[headers['description']], row[headers['passed']],
                    row[headers['num_votes']]]:
                    continue

                ballot_measure = BallotMeasure.get_or_create(election,
                    row[headers['prop_id']])

                ballot_measure.name = row[headers['name']]
                ballot_measure.description = row[headers['description']]
                votes = row[headers['num_votes']].replace(',', '')
                vote_re = re.compile('Yes:\W*(\d+)\W*No:\W*(\d+)')
                ballot_measure.num_yes, ballot_measure.num_no \
                    = vote_re.findall(votes)[0]

                if row[headers['passed']].lower() == 'p':
                    ballot_measure.passed = True
                else:
                    ballot_measure.passed = False

                tag = Tag.get_or_create(row[headers['issue']])
                ballot_type = BallotType.objects.get(name=row[headers['type']].title())

                ballot_measure.tag = tag
                ballot_measure.save()
        except:
            import ipdb;ipdb.set_trace()
            raise