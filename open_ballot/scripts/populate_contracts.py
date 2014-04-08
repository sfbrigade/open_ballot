import csv, re, os
from configparser import ConfigParser
from dateutil import parser
import transaction
from model_patches import (election_get_or_create, consultant_get_or_create,
    committee_get_or_create, ballot_measure_get_or_create)

from open_ballot.models import (BallotMeasure, Committee, Stance,
    Consultant, Contract, Election, DBSession)

Election.get_or_create = election_get_or_create
Consultant.get_or_create = consultant_get_or_create
Committee.get_or_create = committee_get_or_create
BallotMeasure.get_or_create = ballot_measure_get_or_create

def parse_contract_data(input_file):
    if type(input_file) in [str, unicode]:
        input_file = open(input_file)

    reader = csv.DictReader(input_file)
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

    flag = False
    for row in reader:
        try:
            if row[headers['committee_name']] in ['', 'N/A']:
                continue

            with DBSession.no_autoflush:
                election = Election.get_or_create(row[headers['election_date']])
                committee = Committee.get_or_create(
                    name=row[headers['committee_name']],
                    election=election)

                ballot_measure = BallotMeasure.get_or_create(
                    row[headers['prop_id']],
                    election)

                voted_yes = row[headers['stance']].lower().strip() == 'yes'

                stance = DBSession.query(Stance).filter(
                    Stance.committee_id==committee.id,
                    Stance.ballot_measure_id==ballot_measure.id
                    ).first()

                if not stance:
                    stance = Stance(
                        committee=committee,
                        ballot_measure=ballot_measure,
                        voted_yes=voted_yes)
                    name = committee.name

                if not row[headers['consultant']]:
                    transaction.commit()
                    continue
                consultant = Consultant.get_or_create(
                    name=row[headers['consultant']]
                    )

                payment = row[headers['payment']]\
                    .strip().replace('$', '').replace(',', '')

                try:
                    payment = float(payment)
                except ValueError:
                    payment = 0

                Contract(
                    consultant=consultant,
                    committee=committee,
                    payment=payment,
                    description=row[headers['service']]
                    )
                transaction.commit()
        except:
            import ipdb;ipdb.set_trace()
            raise

