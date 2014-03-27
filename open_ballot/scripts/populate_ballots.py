import csv, re, os
from configparser import ConfigParser
from dateutil.parser import parse as date_parse
from datetime import date

from model_patches import election_get_or_create, tag_get_or_create
from open_ballot.models import (BallotMeasure, Election, Tag, BallotType,
    BallotMeasureTag, DBSession)
import transaction

Election.get_or_create = election_get_or_create
Tag.get_or_create = tag_get_or_create

def parse_ballot_data(input_file):
    if type(input_file) in [str, unicode]:
        input_file = open(input_file)

    reader = csv.DictReader(input_file)
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

    for row in reader:
        try:
            election = Election.get_or_create(row[headers['election_date']])

            if '' in [row[headers['description']], row[headers['passed']],
                row[headers['num_votes']]]:
                continue

            ballot_measure = BallotMeasure(election=election)

            ballot_measure.name = row[headers['name']]
            ballot_measure.description = row[headers['description']]
            votes = row[headers['num_votes']].replace(',', '')
            vote_re = re.compile('Yes:\W*(\d+)\W*No:\W*(\d+)')
            ballot_measure.num_yes, ballot_measure.num_no \
                = vote_re.findall(votes)[0]
            ballot_measure.prop_id = row[headers['prop_id']]

            if row[headers['passed']].lower() == 'p':
                ballot_measure.passed = True
            else:
                ballot_measure.passed = False

            tag = Tag.get_or_create(row[headers['issue']])
            ballot_type = DBSession.query(BallotType).filter(
                BallotType.name==row[headers['type']].title()).first()
            if not ballot_type:
                percent_required = row[headers['percent_required']]
                if percent_required == '66 2/3%':
                    percent = 2.0/3
                else:
                    percent = .50

                ballot_type = BallotType(name=row[headers['type']].title(),
                    percent_required=percent)

            ballot_measure.ballot_type = ballot_type
            BallotMeasureTag(ballot_measure=ballot_measure, tag=tag)
            DBSession.add(ballot_measure)
            transaction.commit()
        except:
            import ipdb;ipdb.set_trace()
            raise
